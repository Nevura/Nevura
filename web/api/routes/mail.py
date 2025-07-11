from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from services.mail import send_email_async

router = APIRouter()

class MailRequest(BaseModel):
    to: str
    subject: str
    body: str

@router.post("/send")
async def send_mail(request: MailRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_async, request.to, request.subject, request.body)
    return {"detail": "Email queued for sending"}
