from sqlalchemy.orm import Session

from . import models  # noqa: F401  (registers tables on Base.metadata)
from .data.defaults import (
    DEFAULT_HOLDINGS,
    DEFAULT_INPUT_PROFILE,
    DEFAULT_WATCHLIST,
    DEMO_USER,
)
from .database import Base, SessionLocal, engine
from .models import Holding, RiskProfile, User, WatchlistItem
from .security import hash_password


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_user(db)
    finally:
        db.close()


def seed_user_defaults(db: Session, user: User) -> None:
    db.add(RiskProfile(user_id=user.id, input_profile=dict(DEFAULT_INPUT_PROFILE)))
    for holding in DEFAULT_HOLDINGS:
        db.add(
            Holding(
                user_id=user.id,
                symbol=holding["symbol"],
                quantity=holding["quantity"],
                buy_price=holding["buyPrice"],
            )
        )
    for symbol in DEFAULT_WATCHLIST:
        db.add(WatchlistItem(user_id=user.id, symbol=symbol))


def seed_demo_user(db: Session) -> None:
    if db.query(User).filter(User.email == DEMO_USER["email"]).first():
        return
    user = User(
        name=DEMO_USER["name"],
        email=DEMO_USER["email"],
        password_hash=hash_password(DEMO_USER["password"]),
        broker_connected=DEMO_USER["broker_connected"],
    )
    db.add(user)
    db.flush()
    seed_user_defaults(db, user)
    db.commit()
