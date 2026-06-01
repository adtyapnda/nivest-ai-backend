from fastapi import APIRouter, Depends

from ..deps import get_current_user
from ..models import User
from ..services.news_feed import get_market_news, get_portfolio_news

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/market")
def market_news(user: User = Depends(get_current_user)):
    return get_market_news()


@router.get("/portfolio")
def portfolio_news(user: User = Depends(get_current_user)):
    symbols = [holding.symbol for holding in user.holdings]
    return get_portfolio_news(symbols)
