from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select
from passlib.context import CryptContext
from ..models.user import User
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def generate_api_token(user: User, session: Session) -> str:
        token = secrets.token_urlsafe(32)
        user.api_token = token
        user.token_created_at = datetime.utcnow()
        session.add(user)
        session.commit()
        return token

    @staticmethod
    def get_user_by_token(session: Session, token: str) -> Optional[User]:
        statement = select(User).where(User.api_token == token)
        user = session.exec(statement).first()
        return user

    @staticmethod
    def authenticate(session: Session, username: str, password: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        if user and UserService.verify_password(password, user.hashed_password):
            return user
        return None
