from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlmodel import Session
from ..services.users import UserService
from ..db import get_session  # ta fonction pour récupérer la session DB

security = HTTPBearer()

async def get_current_user(request: Request, session: Session = Depends(get_session)):
    auth = await security.__call__(request)
    token = auth.credentials
    user = UserService.get_user_by_token(session, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API token")
    return user
