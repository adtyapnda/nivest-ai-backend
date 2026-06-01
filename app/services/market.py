"""Stock universe = seeded baseline + live Yahoo Finance quotes.

Live price / changePercent / dayHigh / dayLow are pulled from Yahoo (yfinance)
and cached briefly. On any failure (offline, rate limit, bad ticker) the seeded
values are used so the API always responds.

The custom scores (volatility / momentum / quality) come from `fetch_parasram_scores`
once the Parasram data API is configured; until then the seeded scores are used.
"""
import math
import threading
import time

from ..config import settings
from ..data.stocks import SEED_STOCKS, yahoo_ticker

_CACHE: dict = {"data": None, "ts": 0.0}
_LOCK = threading.Lock()
_TTL_SECONDS = 120


def _num(value) -> float | None:
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) else f


def fetch_parasram_scores() -> dict | None:
    """Seam for the Parasram data API: return {symbol: {volatilityScore, momentumScore, qualityScore}}.

    Not wired yet — returns None so the seeded scores are used.
    """
    if not settings.parasram_api_base or not settings.parasram_api_key:
        return None
    # TODO: call settings.parasram_api_base with PARASRAM_API_KEY and map the response.
    return None


def _fetch_live_quotes() -> dict | None:
    try:
        import yfinance as yf
    except ImportError:
        return None

    symbols = [s["symbol"] for s in SEED_STOCKS]
    tickers = [yahoo_ticker(s) for s in symbols]
    try:
        frame = yf.download(
            tickers,
            period="2d",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False,
            auto_adjust=False,
        )
    except Exception:
        return None

    if frame is None or getattr(frame, "empty", True):
        return None

    quotes: dict = {}
    for symbol, ticker in zip(symbols, tickers):
        try:
            sub = frame[ticker].dropna(how="all")
        except (KeyError, TypeError):
            continue
        if sub is None or sub.empty:
            continue

        last = sub.iloc[-1]
        price = _num(last.get("Close"))
        if price is None:
            continue

        high = _num(last.get("High"))
        low = _num(last.get("Low"))
        open_ = _num(last.get("Open"))

        if len(sub) >= 2:
            prev_close = _num(sub.iloc[-2].get("Close"))
        else:
            prev_close = open_
        change_percent = (
            (price - prev_close) / prev_close * 100 if prev_close else 0.0
        )

        quotes[symbol] = {
            "price": round(price, 2),
            "changePercent": round(change_percent, 2),
            "dayHigh": round(high, 2) if high is not None else round(price, 2),
            "dayLow": round(low, 2) if low is not None else round(price, 2),
        }

    return quotes or None


def _build_universe() -> list[dict]:
    quotes = _fetch_live_quotes() if settings.enable_live_market else None
    scores = fetch_parasram_scores()

    universe = []
    for seed in SEED_STOCKS:
        stock = dict(seed)
        live = quotes.get(stock["symbol"]) if quotes else None
        if live:
            stock.update(live)
        if scores and stock["symbol"] in scores:
            stock.update(scores[stock["symbol"]])
        universe.append(stock)
    return universe


def get_stock_universe() -> list[dict]:
    now = time.time()
    with _LOCK:
        cached = _CACHE["data"]
        if cached is not None and now - _CACHE["ts"] < _TTL_SECONDS:
            return [dict(s) for s in cached]

    universe = _build_universe()

    with _LOCK:
        _CACHE["data"] = universe
        _CACHE["ts"] = time.time()
    return [dict(s) for s in universe]


def get_stock_map() -> dict:
    return {stock["symbol"]: stock for stock in get_stock_universe()}


def build_heatmap() -> list[dict]:
    universe = get_stock_universe()
    heatmap = []
    for stock in universe[:18]:
        item = dict(stock)
        change = stock["changePercent"]
        item["intensity"] = min(
            100, round(abs(change) * 28 + stock["momentumScore"] * 0.35)
        )
        item["tone"] = (
            "positive" if change > 1.2 else "negative" if change < -1.2 else "neutral"
        )
        heatmap.append(item)
    return heatmap
