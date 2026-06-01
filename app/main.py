from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import (
    auth,
    brokers,
    chat,
    market,
    news,
    payments,
    portfolio,
    risk,
    users,
    watchlist,
)
from .seed import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="NivestAI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in (auth, users, risk, portfolio, market, watchlist, news, brokers, payments, chat):
    app.include_router(module.router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"status": "ok", "service": "NivestAI API", "docs": "/docs"}
