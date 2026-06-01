from fastapi import APIRouter, Depends

from ..deps import get_current_user
from ..models import User
from ..schemas import CheckoutRequest
from ..services.payments import create_checkout_session

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/checkout-session")
def checkout_session(payload: CheckoutRequest, user: User = Depends(get_current_user)):
    return create_checkout_session(payload.planName, payload.provider or "razorpay")
