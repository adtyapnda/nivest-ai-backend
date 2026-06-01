import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _flag(name: str, default: str = "1") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    api_prefix = "/api/v1"

    jwt_secret = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_algorithm = "HS256"
    jwt_expire_minutes = int(os.getenv("JWT_EXPIRE_MINUTES", "10080"))

    database_url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'nivest.db'}")

    cors_origins = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]

    enable_live_market = _flag("ENABLE_LIVE_MARKET")
    enable_live_news = _flag("ENABLE_LIVE_NEWS")

    parasram_api_base = os.getenv("PARASRAM_API_BASE", "")
    parasram_api_key = os.getenv("PARASRAM_API_KEY", "")

    razorpay_key_id = os.getenv("RAZORPAY_KEY_ID", "")
    razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET", "")

    groq_api_key = os.getenv("GROQ_API_KEY", "")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


settings = Settings()
