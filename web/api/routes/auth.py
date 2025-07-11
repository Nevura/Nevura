from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import (
    authenticate_user, create_access_token, get_current_user,
    revoke_tokens_for_user, detect_token_anomaly
)
from web.api.models.users import UserRead

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = await create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
async def logout(user=Depends(get_current_user)):
    await revoke_tokens_for_user(user.id)
    return {"detail": "Logged out"}

@router.get("/me", response_model=UserRead)
async def read_current_user(user=Depends(get_current_user)):
    return user

@router.post("/check-token-anomaly")
async def check_token_anomaly(request: Request, user=Depends(get_current_user)):
    anomaly_detected = await detect_token_anomaly(request, user)
    if anomaly_detected:
        raise HTTPException(status_code=403, detail="Token anomaly detected")
    return {"detail": "No anomaly detected"}
