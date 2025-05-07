from fastapi import APIRouter, HTTPException

from sqlmodel import select
from ..models.user import User
from app.db.database import SessionDep
from ..schema.auth import TokenData
from ..utils import create_access_token, create_refresh_token
from loguru import logger
from ..schema.auth import Login


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenData)
def login(login_data: Login, session: SessionDep):
    logger.info(f"{login_data.username}:{login_data.password}")
    statement = select(User).where(User.username == login_data.username)
    user = session.exec(statement).first()
    logger.debug(f"user:{user.verify_password(login_data.password)}")  # type: ignore
    if not user or user.verify_password(login_data.password) is False:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    tokens = TokenData(
        access_token=create_access_token(
            {"username": user.username, "email": user.email, "user_id": user.id}
        ),
        refresh_token=create_refresh_token(
            {"username": user.username, "email": user.email, "user_id": user.id}
        ),
    )

    return tokens
