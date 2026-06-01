from fastapi import APIRouter, Depends

from ..deps import get_current_user
from ..models import User
from ..services.market import build_heatmap, get_stock_universe

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/stocks")
def stocks(user: User = Depends(get_current_user)):
    return get_stock_universe()


@router.get("/heatmap")
def heatmap(user: User = Depends(get_current_user)):
    return build_heatmap()
