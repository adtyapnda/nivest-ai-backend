"""Port of src/engine/riskEngine.js (placeholder model).

Kept numerically faithful to the JS, including JS-style Math.round
(round half up), so the backend score matches the frontend fallback.
"""
import math

from .behavior import detect_fomo, detect_panic_selling


def js_round(value: float) -> int:
    return math.floor(value + 0.5)


def normalize(value: float, low: float, high: float) -> float:
    return max(0.0, min(1.0, (value - low) / (high - low)))


def detect_behavior(profile: dict) -> list[str]:
    fomo = detect_fomo(profile)

    drawdown = profile.get("drawdownReaction")
    if drawdown is None:
        drawdown = profile.get("panicBehavior")
    panic = detect_panic_selling(
        panic_behavior=profile.get("panicBehavior", 0),
        drawdown_reaction=drawdown,
        stop_checking_threshold=8 if profile.get("lossTolerance", 0) <= 10 else 4,
    )

    overconfidence = (
        profile.get("marketExperience", 0) >= 7
        and profile.get("decisionStyle", 0) >= 7
        and profile.get("lossTolerance", 0) >= 18
    )

    flags = [
        "FOMO-driven" if fomo["detected"] else None,
        "Panic-prone" if panic["detected"] else None,
        "Overconfident" if overconfidence else None,
    ]
    return [flag for flag in flags if flag]


def calculate_risk_score(profile: dict) -> dict:
    income_range = profile.get("incomeRange", "")
    portfolio_size_value = profile.get("portfolioSizeValue")
    if portfolio_size_value is None:
        portfolio_size_value = 15

    age_factor = 1 - normalize(profile.get("age", 0), 21, 70)
    horizon_factor = normalize(profile.get("investmentHorizon", 0), 1, 15)
    tolerance_factor = normalize(profile.get("lossTolerance", 0), 5, 35)
    experience_factor = normalize(profile.get("marketExperience", 0), 1, 10)
    income_factor = 0.9 if ("25" in income_range or "30" in income_range) else 0.6
    behavior_penalty = (profile.get("panicBehavior", 0) * 1.2 + profile.get("fomoTendency", 0)) / 20
    activity_penalty = normalize(profile.get("tradingFrequency", 0), 1, 25) * 0.2

    raw_score = (
        age_factor * 16
        + horizon_factor * 18
        + tolerance_factor * 22
        + experience_factor * 14
        + income_factor * 10
        + normalize(profile.get("decisionStyle", 0), 1, 10) * 8
        + normalize(portfolio_size_value, 1, 100) * 8
        - behavior_penalty * 18
        - activity_penalty * 12
    )

    risk_score = max(8, min(92, js_round(raw_score)))
    behavior_flags = detect_behavior(profile)

    risk_category = "Conservative"
    if risk_score >= 65:
        risk_category = "Aggressive"
    elif risk_score >= 40:
        risk_category = "Moderate"

    if risk_category == "Conservative":
        summary = "You appear more comfortable with steadier portfolios and smaller drawdowns."
    elif risk_category == "Moderate":
        summary = "You can handle some market movement, but concentration and sudden sizing still matter."
    else:
        summary = "You can tolerate more volatility, but behavior and allocation discipline still shape suitability."

    return {
        "riskScore": risk_score,
        "riskCategory": risk_category,
        "behaviorFlags": behavior_flags if behavior_flags else ["Balanced behavior"],
        "summary": summary,
    }
