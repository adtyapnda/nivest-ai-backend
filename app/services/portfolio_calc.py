"""Server-side portfolio computation (port of the logic in PortfolioContext.jsx)."""
from ..engines.risk import js_round
from ..engines.suitability import evaluate_stock_suitability


def r2(value: float) -> float:
    return round(value, 2)


def _sector_value(holdings: list[dict], stock_map: dict, sector: str) -> float:
    return sum(
        item["quantity"] * stock_map[item["symbol"]]["price"]
        for item in holdings
        if item["symbol"] in stock_map and stock_map[item["symbol"]]["sector"] == sector
    )


def compute_holdings(holdings: list[dict], stock_map: dict, user_profile: dict) -> list[dict]:
    owned = [item for item in holdings if item["symbol"] in stock_map]
    total_value = sum(item["quantity"] * stock_map[item["symbol"]]["price"] for item in owned)
    if total_value == 0:
        return []

    result = []
    for item in owned:
        stock = stock_map[item["symbol"]]
        current_value = item["quantity"] * stock["price"]
        invested_value = item["quantity"] * item["buyPrice"]
        return_percent = ((current_value - invested_value) / invested_value) * 100 if invested_value else 0.0
        day_change = (stock["changePercent"] / 100) * current_value
        weight = r2((current_value / total_value) * 100)
        sector_weight = r2((_sector_value(owned, stock_map, stock["sector"]) / total_value) * 100)
        suitability = evaluate_stock_suitability(stock, user_profile, weight, sector_weight)

        merged = {**item, **stock}
        merged.update(
            {
                "currentPrice": stock["price"],
                "currentValue": current_value,
                "investedValue": invested_value,
                "returnPercent": r2(return_percent),
                "dayChange": day_change,
                "weight": weight,
                "suitabilityScore": suitability["suitabilityScore"],
            }
        )
        result.append(merged)
    return result


def compute_summary(holdings_computed: list[dict]) -> dict:
    total_value = sum(h["currentValue"] for h in holdings_computed)
    day_change = sum(h["dayChange"] for h in holdings_computed)
    return {
        "totalValue": r2(total_value),
        "dayChange": r2(day_change),
        "dayChangePercent": r2((day_change / total_value) * 100) if total_value else 0.0,
    }


def compute_sector_exposure(holdings_computed: list[dict]) -> list[dict]:
    bucket: dict = {}
    for holding in holdings_computed:
        bucket[holding["sector"]] = bucket.get(holding["sector"], 0) + holding["weight"]
    exposure = [{"name": name, "weight": r2(weight)} for name, weight in bucket.items()]
    exposure.sort(key=lambda entry: entry["weight"], reverse=True)
    return exposure


def compute_reports(holdings_computed: list[dict], sector_exposure: list[dict], user_profile: dict) -> dict:
    top_sector = sector_exposure[0] if sector_exposure else {"name": "Diversified", "weight": 0}

    over_exposed = [
        {
            "symbol": h["symbol"],
            "weight": h["weight"],
            "reason": (
                "Position size is large relative to overall portfolio balance."
                if h["weight"] > 18
                else "Risk level may exceed your profile without careful sizing."
            ),
        }
        for h in holdings_computed
        if h["weight"] > 18 or h["suitabilityScore"] < 55
    ]

    mismatch_count = sum(1 for h in holdings_computed if h["suitabilityScore"] < 55)
    portfolio_score = max(
        32,
        js_round(
            100
            - mismatch_count * 9
            - max(0, top_sector["weight"] - 28) * 0.9
            - max(0, user_profile["riskScore"] - 60) * 0.18
        ),
    )

    if portfolio_score >= 75:
        overview = "Your portfolio appears broadly aligned with your profile."
    elif portfolio_score >= 55:
        overview = "Some allocations may need tightening to stay within comfort range."
    else:
        overview = "Concentration and volatility may be pushing the portfolio beyond your stated tolerance."

    return {
        "portfolioScore": portfolio_score,
        "overview": overview,
        "topSector": top_sector,
        "sectorExposure": sector_exposure,
        "mismatchCount": mismatch_count,
        "riskMismatchSummary": (
            "No position currently stands out as a strong mismatch against your risk profile."
            if mismatch_count == 0
            else f"{mismatch_count} holdings may fluctuate more than your comfort range suggests."
        ),
        "sectorImbalanceSummary": (
            f"{top_sector['name']} is the largest concentration and may reduce diversification resilience."
            if top_sector["weight"] > 30
            else "Sector spread is reasonably balanced, though concentration still deserves monitoring."
        ),
        "overExposureSummary": (
            "A few positions dominate more of the portfolio than ideal for a comfort-led allocation plan."
            if over_exposed
            else "No single position currently dominates the portfolio."
        ),
        "overExposedStocks": over_exposed,
        "suggestions": [
            "Consider reducing single-sector dependence when fresh capital is deployed.",
            "Stagger additions to momentum-heavy names instead of increasing exposure all at once.",
            "Review positions with lower suitability scores before increasing overall risk.",
        ],
    }
