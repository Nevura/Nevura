from sqlmodel import Session, select
from datetime import datetime
from ..db import get_db_session
from ..models.session import UserSession
from ..models.user import User

def get_sessions_for_user(session: Session, user_id: int):
    statement = select(UserSession).where(UserSession.user_id == user_id)
    return session.exec(statement).all()

def revoke_all_sessions(session: Session, user_id: int):
    statement = select(UserSession).where(UserSession.user_id == user_id)
    sessions = session.exec(statement).all()
    for s in sessions:
        session.delete(s)
    session.commit()

def create_session(session: Session, user_id: int, device_info: str, ip_address: str, token: str) -> UserSession:
    new_session = UserSession(
        user_id=user_id,
        device_info=device_info,
        ip_address=ip_address,
        token=token,
        last_active=datetime.utcnow()
    )
    session.add(new_session)
    session.commit()
    session.refresh(new_session)
    return new_session

def find_session(session: Session, user_id: int, device_info: str, ip_address: str) -> UserSession | None:
    statement = select(UserSession).where(
        (UserSession.user_id == user_id) &
        (UserSession.device_info == device_info) &
        (UserSession.ip_address == ip_address)
    )
    return session.exec(statement).first()
