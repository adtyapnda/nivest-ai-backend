"""Port of src/engine/suitabilityEngine.js."""
from .risk import js_round


def evaluate_stock_suitability(stock: dict, user_profile: dict, portfolio_weight: float = 0, sector_weight: float = 0) -> dict:
    behavior_flags = user_profile.get("behaviorFlags", [])

    volatility_gap = max(0, stock["volatilityScore"] - user_profile["riskScore"])
    concentration_penalty = 12 if portfolio_weight > 12 else 7 if portfolio_weight > 8 else 2
    sector_penalty = 10 if sector_weight > 30 else 5 if sector_weight > 20 else 1

    if "FOMO-driven" in behavior_flags:
        behavior_penalty = 12 if stock["momentumScore"] > 75 else 4
    else:
        behavior_penalty = 2

    suitability_score = max(
        18,
        min(
            95,
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

    portfolio_fit = "High" if suitability_score >= 75 else "Medium" if suitability_score >= 55 else "Low"

    if stock["volatilityScore"] <= user_profile["riskScore"] - 5:
        risk_alignment = "Conservative"
    elif stock["volatilityScore"] <= user_profile["riskScore"] + 10:
        risk_alignment = "Moderate"
    else:
        risk_alignment = "Aggressive"

    allocation_range = "4-7%" if suitability_score >= 75 else "2-5%" if suitability_score >= 55 else "0-2%"
    strategy = (
        "Staggered accumulation"
        if suitability_score >= 75
        else "Cautious entry"
        if suitability_score >= 55
        else "Limited exposure"
    )

    if "Panic-prone" in behavior_flags and stock["volatilityScore"] > 65:
        behavior_warning = "Volatility may trigger stress"
    elif "FOMO-driven" in behavior_flags and stock["momentumScore"] > 75:
        behavior_warning = "Momentum chasing risk"
    else:
        behavior_warning = "Position sizing discipline matters"

    guardrail = (
        "This exceeds your comfort range unless position size remains small."
        if suitability_score < 55
        else "Keep any increase aligned with diversification goals."
    )

    return {
        "suitabilityScore": suitability_score,
        "portfolioFit": portfolio_fit,
        "riskAlignment": risk_alignment,
        "allocationRange": allocation_range,
        "strategy": strategy,
        "behaviorWarning": behavior_warning,
        "explanation": "This score reflects volatility, concentration, and how the stock sits within your current comfort range.",
        "guardrail": guardrail,
        "reasoning": "The engine weighs your risk profile, portfolio concentration, and behavior markers against stock volatility and momentum characteristics.",
    }
