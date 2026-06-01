"""Per-user seed defaults (ported from the frontend contexts)."""

# src/context/UserContext.jsx -> defaultInputProfile
DEFAULT_INPUT_PROFILE = {
    "age": 31,
    "incomeRange": "Rs.25L-Rs.40L",
    "portfolioSize": "Rs.15L-Rs.25L",
    "portfolioSizeValue": 18,
    "investmentHorizon": 8,
    "lossTolerance": 16,
    "panicBehavior": 6,
    "fomoTendency": 7,
    "decisionStyle": 6,
    "marketExperience": 7,
    "tradingFrequency": 9,
    "recentChasing": 6,
    "drawdownReaction": 6,
}

# src/data/mockPortfolio.js
DEFAULT_HOLDINGS = [
    {"symbol": "RELIANCE", "quantity": 18, "buyPrice": 2684},
    {"symbol": "HDFCBANK", "quantity": 35, "buyPrice": 1542},
    {"symbol": "INFY", "quantity": 28, "buyPrice": 1440},
    {"symbol": "TCS", "quantity": 9, "buyPrice": 3825},
    {"symbol": "TITAN", "quantity": 10, "buyPrice": 3278},
    {"symbol": "BAJFINANCE", "quantity": 5, "buyPrice": 6812},
    {"symbol": "SUNPHARMA", "quantity": 16, "buyPrice": 1492},
    {"symbol": "TATAMOTORS", "quantity": 24, "buyPrice": 888},
]

# src/context/PortfolioContext.jsx -> initial watchlist
DEFAULT_WATCHLIST = ["RELIANCE", "TCS", "HDFCBANK", "TITAN", "ADANIENT", "SUNPHARMA"]

DEMO_USER = {
    "name": "Aarav Sharma",
    "email": "aarav@nivest.ai",
    "password": "demo1234",
    "broker_connected": True,
}
