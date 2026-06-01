from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from ..models import User

router = APIRouter(prefix="/brokers", tags=["brokers"])


@router.post("/connect")
def connect(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user.broker_connected = True
    db.commit()
    return {
        "connected": True,
        "provider": "Parasram",
        "message": "Broker connected. Live Parasram holdings sync is pending the broker API.",
    }
