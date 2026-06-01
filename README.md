# NivestAI backend

FastAPI service that powers the NivestAI frontend at
[nivestai-demo-38721.netlify.app](https://nivestai-demo-38721.netlify.app).

## What it provides

- **JWT auth** (`/auth/login`, `/auth/signup`) with SQLite persistence
- **Risk engine** (`/risk/profile`, `/risk/calculate`) — port of the JS scoring engine
- **Portfolio** (`/portfolio/holdings | summary | reports`) — server-side suitability + sector exposure
- **Live NSE market data** (`/market/stocks`, `/market/heatmap`) via `yfinance`
- **Watchlist**, **News** (Tickertape best-effort + seeded fallback)
- **Razorpay-ready checkout stub**
- **Groq-backed `/chat`** with a stocks-only system prompt

## One-click deploy on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Click the button, sign in with GitHub, select this repo. Render reads
`render.yaml`, builds the Docker image, and serves on a `*.onrender.com`
URL. Free plan sleeps after 15 min idle — first request after sleep takes
~30s.

Required env var to set in the Render dashboard:
- `GROQ_API_KEY` — get one at [console.groq.com/keys](https://console.groq.com/keys)

Optional:
- `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` — live checkout instead of stub
- `PARASRAM_API_BASE` / `PARASRAM_API_KEY` — when the friend's API is ready

## Local development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The seed user `aarav@nivest.ai / demo1234` is created automatically on first run.
