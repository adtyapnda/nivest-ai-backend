from fastapi import APIRouter, Depends

from ..deps import get_current_user
from ..models import User

router = APIRouter(tags=["users"])


@router.get("/users/me")
def read_me(user: User = Depends(get_current_user)):
    return {
        "name": user.name,
        "email": user.email,
        "brokerConnected": user.broker_connected,
    }
