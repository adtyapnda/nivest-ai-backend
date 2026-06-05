"""Groq-backed chat with a stocks-only system prompt."""
import httpx

from ..config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """\
You are NivestAI, an assistant for Indian retail investors.

STRICT TOPIC RESTRICTION
You ONLY discuss: stocks, equity markets (NSE / BSE), mutual funds, ETFs, sectors,
indices (NIFTY 50, SENSEX, etc.), portfolio construction, position sizing,
diversification, risk profiling, behavioral investing (FOMO, panic selling,
overconfidence), suitability, fundamental & technical concepts, broker mechanics,
SIPs, taxation of equity, and macroeconomic factors that materially affect Indian
markets (RBI policy, inflation, crude, currency, fiscal policy).

If the user asks about ANYTHING else — coding, recipes, sports, weather, general
trivia, personal life advice, other countries' markets unless tied to India,
crypto/forex specifics, gambling, etc. — refuse politely in ONE sentence and
redirect them to an investing topic. Example refusal:
"I only help with stocks and Indian-market investing — want me to look at a
holding or a sector in your portfolio instead?"

COMPLIANCE
You are NOT a SEBI-registered investment advisor. NEVER give specific buy / sell
calls, price targets, or guaranteed-return claims. Give analytical / educational
perspective only. Mention that the user should consider their own risk profile.

STYLE
- 2-5 sentences. No fluff, no preambles like "Great question".
- Use ₹ for prices. Refer to NSE tickers as RELIANCE, TCS, INFY, etc.
- If you don't know, say so plainly.
"""


class ChatConfigError(Exception):
    pass


def _system_prompt_with_profile(profile: dict | None) -> str:
    if not profile:
        return SYSTEM_PROMPT
    rs = profile.get("riskScore", "unknown")
    cat = profile.get("riskCategory", "unknown")
    flags = profile.get("behaviorFlags") or []
    flag_text = ", ".join(flags) if flags else "none"
    summary = profile.get("summary", "")
    extra = (
        "\n\nUSER PROFILE CONTEXT (use this to tailor every answer)\n"
        f"Risk score (0-100): {rs}\n"
        f"Risk category: {cat}\n"
        f"Behavior flags: {flag_text}\n"
        + (f"Profile summary: {summary}\n" if summary else "")
        + "When the user asks about a stock or sector, weigh your answer against their risk score and behavior flags. "
        "If they're FOMO-driven, gently slow down momentum recommendations. If they're Panic-prone, mention drawdown risk early."
    )
    return SYSTEM_PROMPT + extra


def chat_completion(message: str, history: list[dict] | None = None, profile: dict | None = None) -> str:
    if not settings.groq_api_key:
        raise ChatConfigError(
            "GROQ_API_KEY is not set. Add it to backend/.env to enable chat."
        )

    messages = [{"role": "system", "content": _system_prompt_with_profile(profile)}]
    if history:
        for msg in history[-8:]:
            role = msg.get("role")
            content = msg.get("content")
            if role in ("user", "assistant") and isinstance(content, str):
                messages.append({"role": role, "content": content})
    # Ensure the latest user message is appended (history may already include it).
    if not messages[-1].get("role") == "user" or messages[-1].get("content") != message:
        messages.append({"role": "user", "content": message})

    payload = {
        "model": settings.groq_model,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 500,
    }
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }

    response = httpx.post(GROQ_URL, json=payload, headers=headers, timeout=30)
    if response.status_code >= 400:
        raise RuntimeError(f"Groq error {response.status_code}: {response.text[:200]}")

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
