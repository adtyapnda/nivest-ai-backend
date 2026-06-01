from fastapi import APIRouter, Depends

from ..data.defaults import DEFAULT_INPUT_PROFILE
from ..deps import get_current_user
from ..engines.risk import calculate_risk_score
from ..models import User
from ..services.market import get_stock_map
from ..services.portfolio_calc import (
    compute_holdings,
    compute_reports,
    compute_sector_exposure,
    compute_summary,
)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


def _user_risk(user: User) -> dict:
    input_profile = user.risk_profile.input_profile if user.risk_profile else dict(DEFAULT_INPUT_PROFILE)
    return {"inputProfile": input_profile, **calculate_risk_score(input_profile)}


def _raw_holdings(user: User) -> list[dict]:
    return [
        {"symbol": h.symbol, "quantity": h.quantity, "buyPrice": h.buy_price}
        for h in user.holdings
    ]


@router.get("/holdings")
def holdings(user: User = Depends(get_current_user)):
    return compute_holdings(_raw_holdings(user), get_stock_map(), _user_risk(user))


@router.get("/summary")
def summary(user: User = Depends(get_current_user)):
    computed = compute_holdings(_raw_holdings(user), get_stock_map(), _user_risk(user))
    return compute_summary(computed)


@router.get("/reports")
def reports(user: User = Depends(get_current_user)):
    risk = _user_risk(user)
    computed = compute_holdings(_raw_holdings(user), get_stock_map(), risk)
    sector_exposure = compute_sector_exposure(computed)
    return compute_reports(computed, sector_exposure, risk)
