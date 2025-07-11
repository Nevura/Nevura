from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from ..services.mail import send_email, test_smtp
from sqlmodel import Session
from ..db import get_session

router = APIRouter()

class MailTestRequest(BaseModel):
    email: EmailStr

@router.post("/test")
async def test_mail(data: MailTestRequest, session: Session = Depends(get_session)):
    return await test_smtp(data.email, session)
