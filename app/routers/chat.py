from fastapi import APIRouter, Body, HTTPException, status

from ..services.chat import ChatConfigError, chat_completion

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
def chat(payload: dict = Body(...)):
    message = (payload.get("message") or "").strip()
    history = payload.get("history") or []
    if not message:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="message is required")
    try:
        reply = chat_completion(message, history)
    except ChatConfigError as error:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, detail=str(error))
    return {"response": reply}
