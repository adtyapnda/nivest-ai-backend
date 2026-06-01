"""Port of src/engine/behaviorEngine.js (placeholder model)."""


def detect_fomo(profile: dict) -> dict:
    fomo_tendency = profile.get("fomoTendency", 0) or 0
    trading_frequency = profile.get("tradingFrequency", 0) or 0
    recent_chasing = profile.get("recentChasing", 0) or 0
    score = fomo_tendency * 0.5 + trading_frequency * 0.25 + recent_chasing * 0.25
    return {"score": min(100, round(score * 10)), "detected": score >= 6}


def detect_panic_selling(panic_behavior=0, drawdown_reaction=0, stop_checking_threshold=0) -> dict:
    panic_behavior = panic_behavior or 0
    drawdown_reaction = drawdown_reaction or 0
    stop_checking_threshold = stop_checking_threshold or 0
    score = panic_behavior * 0.55 + drawdown_reaction * 0.3 + stop_checking_threshold * 0.15
    return {"score": min(100, round(score * 10)), "detected": score >= 5.5}
