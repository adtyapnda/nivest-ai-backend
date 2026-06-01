"""Market news via Tickertape (best-effort), with seeded fallback.

Portfolio and deal news stay curated (seeded). The market feed pulls live
headlines from Tickertape when reachable; any failure falls back to the seeded
market news so the endpoints always respond.
"""
import threading
import time

from ..config import settings
from ..data.news import SEED_NEWS

_TICKERTAPE_NEWS_URL = "https://api.tickertape.in/news/feed"
_CACHE: dict = {"data": None, "ts": 0.0}
_LOCK = threading.Lock()
_TTL_SECONDS = 300


def _seeded(category: str) -> list[dict]:
    return [dict(item) for item in SEED_NEWS if item["category"] == category]


def _parse_tickertape(payload) -> list[dict]:
    if isinstance(payload, dict):
        for key in ("data", "items", "news", "feed", "results"):
            if isinstance(payload.get(key), list):
                payload = payload[key]
                break
    if not isinstance(payload, list):
        return []

    items = []
    for index, raw in enumerate(payload):
        if not isinstance(raw, dict):
            continue
        title = raw.get("headline") or raw.get("title") or raw.get("name")
        if not title:
            continue
        summary = raw.get("summary") or raw.get("description") or raw.get("snippet") or ""
        items.append(
            {
                "id": str(raw.get("id") or raw.get("_id") or f"tt-{index}"),
                "category": "market",
                "symbols": [],
                "title": title,
                "summary": summary,
                "impact": "Live market headline",
            }
        )
        if len(items) >= 8:
            break
    return items


def _fetch_tickertape_market_news() -> list[dict] | None:
    try:
        import httpx
    except ImportError:
        return None
    try:
        response = httpx.get(
            _TICKERTAPE_NEWS_URL,
            timeout=6.0,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
        )
        response.raise_for_status()
        items = _parse_tickertape(response.json())
    except Exception:
        return None
    return items or None


def get_market_news() -> list[dict]:
    if not settings.enable_live_news:
        return _seeded("market")

    now = time.time()
    with _LOCK:
        cached = _CACHE["data"]
        if cached is not None and now - _CACHE["ts"] < _TTL_SECONDS:
            return [dict(item) for item in cached]

    live = _fetch_tickertape_market_news()
    news = live if live else _seeded("market")

    with _LOCK:
        _CACHE["data"] = news
        _CACHE["ts"] = time.time()
    return [dict(item) for item in news]


def get_portfolio_news(portfolio_symbols: list[str]) -> list[dict]:
    symbol_set = set(portfolio_symbols)
    return [
        item
        for item in _seeded("portfolio")
        if any(symbol in symbol_set for symbol in item["symbols"])
    ]
