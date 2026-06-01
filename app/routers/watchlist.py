from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import User, WatchlistItem

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


def _symbols(db: Session, user_id: int) -> list[str]:
    rows = db.query(WatchlistItem.symbol).filter(WatchlistItem.user_id == user_id).all()
    return [row[0] for row in rows]


@router.get("")
def get_watchlist(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _symbols(db, user.id)


@router.post("/{symbol}")
def add_symbol(symbol: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    exists = (
        db.query(WatchlistItem)
        .filter(WatchlistItem.user_id == user.id, WatchlistItem.symbol == symbol)
        .first()
    )
    if not exists:
        db.add(WatchlistItem(user_id=user.id, symbol=symbol))
        db.commit()
    return _symbols(db, user.id)


@router.delete("/{symbol}")
def remove_symbol(symbol: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = (
        db.query(WatchlistItem)
        .filter(WatchlistItem.user_id == user.id, WatchlistItem.symbol == symbol)
        .first()
    )
    if item:
        db.delete(item)
        db.commit()
    return _symbols(db, user.id)
