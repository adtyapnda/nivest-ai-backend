"""Seeded stock universe (port of src/data/mockStocks.js).

price / changePercent / dayHigh / dayLow are refreshed from live data
(Yahoo Finance) at request time; the values here are the offline fallback.
volatilityScore / momentumScore / qualityScore are the seeded baseline until
the Parasram data API is wired in.
"""

SEED_STOCKS = [
    {"symbol": "RELIANCE", "name": "Reliance Industries", "sector": "Energy", "price": 2956, "changePercent": 1.2, "dayHigh": 2974, "dayLow": 2918, "volatilityScore": 58, "momentumScore": 64, "qualityScore": 82},
    {"symbol": "TCS", "name": "Tata Consultancy Services", "sector": "IT", "price": 4018, "changePercent": -0.6, "dayHigh": 4042, "dayLow": 3980, "volatilityScore": 44, "momentumScore": 51, "qualityScore": 88},
    {"symbol": "HDFCBANK", "name": "HDFC Bank", "sector": "Financials", "price": 1689, "changePercent": 0.8, "dayHigh": 1701, "dayLow": 1668, "volatilityScore": 42, "momentumScore": 48, "qualityScore": 86},
    {"symbol": "INFY", "name": "Infosys", "sector": "IT", "price": 1525, "changePercent": 1.6, "dayHigh": 1538, "dayLow": 1498, "volatilityScore": 47, "momentumScore": 57, "qualityScore": 84},
    {"symbol": "ICICIBANK", "name": "ICICI Bank", "sector": "Financials", "price": 1184, "changePercent": 0.5, "dayHigh": 1193, "dayLow": 1168, "volatilityScore": 46, "momentumScore": 55, "qualityScore": 83},
    {"symbol": "SBIN", "name": "State Bank of India", "sector": "Financials", "price": 826, "changePercent": -0.9, "dayHigh": 838, "dayLow": 819, "volatilityScore": 57, "momentumScore": 52, "qualityScore": 74},
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel", "sector": "Telecom", "price": 1432, "changePercent": 0.7, "dayHigh": 1446, "dayLow": 1411, "volatilityScore": 49, "momentumScore": 59, "qualityScore": 81},
    {"symbol": "LT", "name": "Larsen & Toubro", "sector": "Industrials", "price": 3721, "changePercent": 1.1, "dayHigh": 3736, "dayLow": 3665, "volatilityScore": 51, "momentumScore": 61, "qualityScore": 80},
    {"symbol": "ITC", "name": "ITC", "sector": "Consumer", "price": 438, "changePercent": -0.4, "dayHigh": 442, "dayLow": 435, "volatilityScore": 33, "momentumScore": 39, "qualityScore": 77},
    {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank", "sector": "Financials", "price": 1836, "changePercent": 0.4, "dayHigh": 1850, "dayLow": 1814, "volatilityScore": 45, "momentumScore": 46, "qualityScore": 79},
    {"symbol": "ASIANPAINT", "name": "Asian Paints", "sector": "Consumer", "price": 2862, "changePercent": -1.2, "dayHigh": 2890, "dayLow": 2836, "volatilityScore": 40, "momentumScore": 35, "qualityScore": 78},
    {"symbol": "AXISBANK", "name": "Axis Bank", "sector": "Financials", "price": 1138, "changePercent": 0.6, "dayHigh": 1149, "dayLow": 1122, "volatilityScore": 48, "momentumScore": 50, "qualityScore": 78},
    {"symbol": "MARUTI", "name": "Maruti Suzuki", "sector": "Auto", "price": 12424, "changePercent": 0.9, "dayHigh": 12498, "dayLow": 12286, "volatilityScore": 43, "momentumScore": 60, "qualityScore": 83},
    {"symbol": "SUNPHARMA", "name": "Sun Pharma", "sector": "Healthcare", "price": 1712, "changePercent": 1.4, "dayHigh": 1728, "dayLow": 1689, "volatilityScore": 46, "momentumScore": 63, "qualityScore": 82},
    {"symbol": "HCLTECH", "name": "HCL Technologies", "sector": "IT", "price": 1628, "changePercent": 0.2, "dayHigh": 1641, "dayLow": 1606, "volatilityScore": 45, "momentumScore": 54, "qualityScore": 80},
    {"symbol": "ULTRACEMCO", "name": "UltraTech Cement", "sector": "Materials", "price": 10218, "changePercent": -0.7, "dayHigh": 10300, "dayLow": 10144, "volatilityScore": 41, "momentumScore": 47, "qualityScore": 79},
    {"symbol": "TITAN", "name": "Titan Company", "sector": "Consumer", "price": 3474, "changePercent": 1.8, "dayHigh": 3490, "dayLow": 3412, "volatilityScore": 54, "momentumScore": 72, "qualityScore": 81},
    {"symbol": "BAJFINANCE", "name": "Bajaj Finance", "sector": "Financials", "price": 7196, "changePercent": 2.1, "dayHigh": 7238, "dayLow": 7048, "volatilityScore": 63, "momentumScore": 78, "qualityScore": 80},
    {"symbol": "NESTLEIND", "name": "Nestle India", "sector": "Consumer", "price": 2468, "changePercent": -0.3, "dayHigh": 2481, "dayLow": 2450, "volatilityScore": 36, "momentumScore": 44, "qualityScore": 84},
    {"symbol": "POWERGRID", "name": "Power Grid Corp", "sector": "Utilities", "price": 316, "changePercent": 0.5, "dayHigh": 319, "dayLow": 312, "volatilityScore": 29, "momentumScore": 42, "qualityScore": 76},
    {"symbol": "NTPC", "name": "NTPC", "sector": "Utilities", "price": 368, "changePercent": 1.2, "dayHigh": 371, "dayLow": 362, "volatilityScore": 32, "momentumScore": 53, "qualityScore": 75},
    {"symbol": "ONGC", "name": "ONGC", "sector": "Energy", "price": 276, "changePercent": -0.5, "dayHigh": 279, "dayLow": 272, "volatilityScore": 56, "momentumScore": 58, "qualityScore": 72},
    {"symbol": "TATAMOTORS", "name": "Tata Motors", "sector": "Auto", "price": 1024, "changePercent": 1.9, "dayHigh": 1032, "dayLow": 995, "volatilityScore": 68, "momentumScore": 81, "qualityScore": 74},
    {"symbol": "M&M", "name": "Mahindra & Mahindra", "sector": "Auto", "price": 2568, "changePercent": 1.3, "dayHigh": 2592, "dayLow": 2522, "volatilityScore": 57, "momentumScore": 69, "qualityScore": 79},
    {"symbol": "TATASTEEL", "name": "Tata Steel", "sector": "Materials", "price": 167, "changePercent": -1.5, "dayHigh": 171, "dayLow": 165, "volatilityScore": 70, "momentumScore": 65, "qualityScore": 69},
    {"symbol": "WIPRO", "name": "Wipro", "sector": "IT", "price": 487, "changePercent": -0.8, "dayHigh": 492, "dayLow": 482, "volatilityScore": 49, "momentumScore": 43, "qualityScore": 73},
    {"symbol": "BAJAJFINSV", "name": "Bajaj Finserv", "sector": "Financials", "price": 1718, "changePercent": 1.1, "dayHigh": 1732, "dayLow": 1686, "volatilityScore": 60, "momentumScore": 71, "qualityScore": 78},
    {"symbol": "ADANIENT", "name": "Adani Enterprises", "sector": "Industrials", "price": 3228, "changePercent": 2.6, "dayHigh": 3262, "dayLow": 3130, "volatilityScore": 82, "momentumScore": 88, "qualityScore": 66},
    {"symbol": "ADANIPORTS", "name": "Adani Ports", "sector": "Industrials", "price": 1462, "changePercent": 1.7, "dayHigh": 1478, "dayLow": 1426, "volatilityScore": 61, "momentumScore": 74, "qualityScore": 75},
    {"symbol": "COALINDIA", "name": "Coal India", "sector": "Energy", "price": 456, "changePercent": 0.6, "dayHigh": 460, "dayLow": 449, "volatilityScore": 37, "momentumScore": 49, "qualityScore": 72},
    {"symbol": "INDUSINDBK", "name": "IndusInd Bank", "sector": "Financials", "price": 1414, "changePercent": -1.1, "dayHigh": 1438, "dayLow": 1402, "volatilityScore": 64, "momentumScore": 45, "qualityScore": 68},
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever", "sector": "Consumer", "price": 2514, "changePercent": -0.2, "dayHigh": 2524, "dayLow": 2486, "volatilityScore": 34, "momentumScore": 40, "qualityScore": 85},
    {"symbol": "DRREDDY", "name": "Dr. Reddy's", "sector": "Healthcare", "price": 6542, "changePercent": 0.9, "dayHigh": 6580, "dayLow": 6468, "volatilityScore": 42, "momentumScore": 56, "qualityScore": 83},
    {"symbol": "EICHERMOT", "name": "Eicher Motors", "sector": "Auto", "price": 4828, "changePercent": 1.1, "dayHigh": 4860, "dayLow": 4770, "volatilityScore": 48, "momentumScore": 61, "qualityScore": 80},
    {"symbol": "GRASIM", "name": "Grasim Industries", "sector": "Materials", "price": 2724, "changePercent": 0.7, "dayHigh": 2740, "dayLow": 2688, "volatilityScore": 46, "momentumScore": 52, "qualityScore": 77},
    {"symbol": "HEROMOTOCO", "name": "Hero MotoCorp", "sector": "Auto", "price": 5412, "changePercent": -0.6, "dayHigh": 5440, "dayLow": 5368, "volatilityScore": 44, "momentumScore": 50, "qualityScore": 76},
    {"symbol": "JSWSTEEL", "name": "JSW Steel", "sector": "Materials", "price": 948, "changePercent": -1.2, "dayHigh": 960, "dayLow": 939, "volatilityScore": 62, "momentumScore": 57, "qualityScore": 71},
    {"symbol": "BPCL", "name": "BPCL", "sector": "Energy", "price": 618, "changePercent": 0.3, "dayHigh": 623, "dayLow": 610, "volatilityScore": 51, "momentumScore": 46, "qualityScore": 70},
    {"symbol": "CIPLA", "name": "Cipla", "sector": "Healthcare", "price": 1514, "changePercent": 0.8, "dayHigh": 1528, "dayLow": 1492, "volatilityScore": 39, "momentumScore": 52, "qualityScore": 79},
    {"symbol": "DIVISLAB", "name": "Divi's Labs", "sector": "Healthcare", "price": 3862, "changePercent": 1.5, "dayHigh": 3888, "dayLow": 3804, "volatilityScore": 41, "momentumScore": 60, "qualityScore": 84},
    {"symbol": "APOLLOHOSP", "name": "Apollo Hospitals", "sector": "Healthcare", "price": 6640, "changePercent": 1.6, "dayHigh": 6682, "dayLow": 6554, "volatilityScore": 50, "momentumScore": 68, "qualityScore": 83},
    {"symbol": "TECHM", "name": "Tech Mahindra", "sector": "IT", "price": 1322, "changePercent": -0.7, "dayHigh": 1338, "dayLow": 1306, "volatilityScore": 51, "momentumScore": 48, "qualityScore": 74},
    {"symbol": "HDFCLIFE", "name": "HDFC Life", "sector": "Financials", "price": 648, "changePercent": 0.2, "dayHigh": 652, "dayLow": 640, "volatilityScore": 38, "momentumScore": 47, "qualityScore": 75},
    {"symbol": "SBILIFE", "name": "SBI Life", "sector": "Financials", "price": 1538, "changePercent": 0.3, "dayHigh": 1548, "dayLow": 1518, "volatilityScore": 36, "momentumScore": 45, "qualityScore": 78},
    {"symbol": "BRITANNIA", "name": "Britannia Industries", "sector": "Consumer", "price": 5180, "changePercent": 0.5, "dayHigh": 5204, "dayLow": 5122, "volatilityScore": 35, "momentumScore": 49, "qualityScore": 82},
    {"symbol": "SHRIRAMFIN", "name": "Shriram Finance", "sector": "Financials", "price": 2466, "changePercent": 1.9, "dayHigh": 2482, "dayLow": 2410, "volatilityScore": 66, "momentumScore": 76, "qualityScore": 73},
    {"symbol": "BAJAJ-AUTO", "name": "Bajaj Auto", "sector": "Auto", "price": 9204, "changePercent": 0.8, "dayHigh": 9246, "dayLow": 9120, "volatilityScore": 42, "momentumScore": 58, "qualityScore": 81},
    {"symbol": "LTIM", "name": "LTIMindtree", "sector": "IT", "price": 5468, "changePercent": -0.9, "dayHigh": 5510, "dayLow": 5418, "volatilityScore": 53, "momentumScore": 55, "qualityScore": 77},
    {"symbol": "HINDALCO", "name": "Hindalco Industries", "sector": "Materials", "price": 688, "changePercent": -1.4, "dayHigh": 699, "dayLow": 682, "volatilityScore": 65, "momentumScore": 59, "qualityScore": 70},
    {"symbol": "TATACONSUM", "name": "Tata Consumer", "sector": "Consumer", "price": 1188, "changePercent": 0.4, "dayHigh": 1194, "dayLow": 1172, "volatilityScore": 38, "momentumScore": 51, "qualityScore": 78},
]

SEED_STOCK_MAP = {stock["symbol"]: stock for stock in SEED_STOCKS}

# NSE symbols map to Yahoo tickers by appending ".NS".
def yahoo_ticker(symbol: str) -> str:
    return f"{symbol}.NS"
