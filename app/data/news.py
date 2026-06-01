"""Seeded news (port of src/data/mockNews.js).

Used as the offline fallback when live Tickertape news is unavailable, and
as the permanent source for the "deal" category.
"""

SEED_NEWS = [
    {"id": "n1", "category": "portfolio", "symbols": ["RELIANCE"], "title": "Reliance expands new energy commissioning timeline", "summary": "Execution progress may support long-term visibility, though the project cycle can still create short-term swings.", "impact": "Moderate portfolio relevance"},
    {"id": "n2", "category": "portfolio", "symbols": ["HDFCBANK"], "title": "Private banks see improving deposit traction", "summary": "Funding conditions look steadier, which can support balance-sheet resilience across large lenders.", "impact": "High portfolio relevance"},
    {"id": "n3", "category": "portfolio", "symbols": ["TATAMOTORS"], "title": "Auto demand commentary remains mixed ahead of festive season", "summary": "Momentum remains positive, but cyclical stocks may fluctuate faster than low-volatility holdings.", "impact": "Behavior watch"},
    {"id": "n4", "category": "market", "symbols": [], "title": "RBI policy tone remains data-sensitive", "summary": "Rate expectations continue to shape banking, valuation multiples, and retail risk appetite.", "impact": "Macro watch"},
    {"id": "n5", "category": "market", "symbols": [], "title": "Crude prices stay rangebound after global supply commentary", "summary": "Energy and transport-linked names may react unevenly as input assumptions shift.", "impact": "Sector sensitivity"},
    {"id": "n6", "category": "deal", "symbols": [], "title": "Large-cap IT deal wins pick up for export-heavy players", "summary": "Order momentum can improve confidence, but earnings delivery still matters more than headlines.", "impact": "Watch for optimism spikes"},
    {"id": "n7", "category": "deal", "symbols": [], "title": "Domestic mutual fund flows remain supportive in large caps", "summary": "Stable flows can reduce pressure, though they do not remove valuation risk.", "impact": "Broad market support"},
]
