from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from ..data.defaults import DEFAULT_INPUT_PROFILE
from ..database import get_db
from ..deps import get_current_user
from ..engines.risk import calculate_risk_score
from ..models import RiskProfile, User

router = APIRouter(prefix="/risk", tags=["risk"])


def _profile_response(input_profile: dict) -> dict:
    return {"inputProfile": input_profile, **calculate_risk_score(input_profile)}


@router.get("/profile")
def get_profile(user: User = Depends(get_current_user)):
    input_profile = user.risk_profile.input_profile if user.risk_profile else dict(DEFAULT_INPUT_PROFILE)
    return _profile_response(input_profile)


@router.post("/calculate")
def calculate(
    profile: dict = Body(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    base = dict(user.risk_profile.input_profile) if user.risk_profile else dict(DEFAULT_INPUT_PROFILE)
    base.update(profile or {})

    if user.risk_profile:
        user.risk_profile.input_profile = base
    else:
        db.add(RiskProfile(user_id=user.id, input_profile=base))
    db.commit()
    return _profile_response(base)
