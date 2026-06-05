"""Port of src/engine/suitabilityEngine.js (varied per-stock commentary)."""
from .risk import js_round


def _describe_volatility(v: float) -> str:
    if v >= 70: return "high"
    if v >= 50: return "moderate"
    if v >= 35: return "contained"
    return "low"


def _describe_momentum(m: float) -> str:
    if m >= 75: return "running hot"
    if m >= 60: return "trending up"
    if m >= 45: return "steady"
    if m >= 30: return "cooling off"
    return "flat"


def _describe_quality(q: float) -> str:
    if q >= 82: return "high-quality"
    if q >= 70: return "solid"
    if q >= 60: return "average-quality"
    return "lower-quality"


def _build_commentary(stock: dict, user_profile: dict, portfolio_weight: float, sector_weight: float) -> str:
    lines = []
    vol = _describe_volatility(stock["volatilityScore"])
    mom = _describe_momentum(stock["momentumScore"])
    qual = _describe_quality(stock["qualityScore"])
    sector = stock["sector"]
    sector_lower = sector.lower()
    risk_gap = stock["volatilityScore"] - user_profile["riskScore"]

    # Opening
    if qual == "high-quality" and vol == "low":
        lines.append(f"{stock['name']} is a defensive {sector_lower} name. Quality reads {stock['qualityScore']} out of 100 and volatility stays low.")
    elif vol == "high" and mom == "running hot":
        lines.append(f"{stock['name']} is one of the more volatile {sector_lower} names and momentum is running hot at {stock['momentumScore']} out of 100.")
    elif vol == "high":
        lines.append(f"{stock['name']} carries a {vol} volatility profile for the {sector_lower} space.")
    elif mom == "running hot":
        lines.append(f"{stock['name']} has been on a strong run. Momentum is {mom} at {stock['momentumScore']} out of 100.")
    elif mom in ("cooling off", "flat"):
        lines.append(f"{stock['name']} has slowed down lately. Momentum sits at {stock['momentumScore']} out of 100 in the {sector_lower} space.")
    else:
        lines.append(f"{stock['name']} is a {qual} {sector_lower} name with {vol} volatility and {mom} momentum.")

    # Risk alignment
    cat = user_profile.get("riskCategory", "moderate").lower()
    rs = user_profile["riskScore"]
    if risk_gap <= -15:
        lines.append(f"Sits well inside your {cat} comfort range so the day-to-day swings should be easy to sit through.")
    elif risk_gap <= -5:
        lines.append(f"Slightly calmer than your {cat} profile, so it shouldn't add stress to the book.")
    elif risk_gap <= 8:
        lines.append(f"Tracks close to your risk score of {rs}, so it fits how you already invest.")
    elif risk_gap <= 18:
        lines.append(f"Runs a notch above your risk score of {rs}. Manageable, but keep the position size sensible.")
    else:
        lines.append(f"Runs well above your risk score of {rs}, so this is the kind of name where position sizing really matters.")

    flags = user_profile.get("behaviorFlags", []) or []
    if "FOMO-driven" in flags and stock["momentumScore"] > 75:
        lines.append("Given your FOMO flag, slow the entry down. Don't add the whole position on a green day.")
    elif "Panic-prone" in flags and stock["volatilityScore"] > 65:
        lines.append("Drawdowns here can be sharp. Easy to panic out at exactly the wrong moment.")
    elif sector_weight > 28:
        lines.append(f"Your portfolio is already {round(sector_weight)} percent in {sector_lower}. Adding more leans on a single sector.")
    elif portfolio_weight > 14:
        lines.append(f"This is already a meaningful position at {round(portfolio_weight)} percent. Adding more concentrates the book.")
    elif qual == "lower-quality":
        lines.append(f"Quality is on the lower end of the index at {stock['qualityScore']} out of 100. Worth checking the latest results before sizing up.")

    return " ".join(lines)


def evaluate_stock_suitability(stock: dict, user_profile: dict, portfolio_weight: float = 0, sector_weight: float = 0) -> dict:
    behavior_flags = user_profile.get("behaviorFlags", []) or []

    volatility_gap = max(0, stock["volatilityScore"] - user_profile["riskScore"])
    concentration_penalty = 12 if portfolio_weight > 12 else 7 if portfolio_weight > 8 else 2
    sector_penalty = 10 if sector_weight > 30 else 5 if sector_weight > 20 else 1

    if "FOMO-driven" in behavior_flags:
        behavior_penalty = 12 if stock["momentumScore"] > 75 else 4
    else:
        behavior_penalty = 2

    suitability_score = max(
        12,
        min(
            100,
            js_round(
                100
                - volatility_gap * 0.55
                - concentration_penalty
                - sector_penalty
                - behavior_penalty
                + stock["qualityScore"] * 0.12
            ),
        ),
    )

    if suitability_score >= 78:
        portfolio_fit = "Strong fit"
        allocation_range = "4 to 7 percent"
    elif suitability_score >= 60:
        portfolio_fit = "Reasonable fit"
        allocation_range = "2 to 5 percent"
    elif suitability_score >= 45:
        portfolio_fit = "Mixed fit"
        allocation_range = "1 to 3 percent"
    else:
        portfolio_fit = "Poor fit"
        allocation_range = "up to 1 percent if any"

    if stock["volatilityScore"] <= user_profile["riskScore"] - 8:
        risk_alignment = "Calmer than you"
    elif stock["volatilityScore"] <= user_profile["riskScore"] + 10:
        risk_alignment = "In line with you"
    else:
        risk_alignment = "Hotter than you"

    commentary = _build_commentary(stock, user_profile, portfolio_weight, sector_weight)
    headline = commentary.split(". ")[0]
    if "." in commentary:
        headline = headline + "."

    if suitability_score < 50:
        guardrail = "If you go ahead, keep the position small. This one doesn't sit easily inside your profile."
    else:
        guardrail = "Tighten the entry if the position would push your sector or risk targets."

    return {
        "suitabilityScore": suitability_score,
        "portfolioFit": portfolio_fit,
        "riskAlignment": risk_alignment,
        "allocationRange": allocation_range,
        "commentary": commentary,
        "headline": headline,
        "strategy": portfolio_fit,
        "behaviorWarning": headline,
        "explanation": commentary,
        "guardrail": guardrail,
        "reasoning": commentary,
    }
