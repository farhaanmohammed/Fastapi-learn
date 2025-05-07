import os
from datetime import datetime, timedelta
import jwt
from loguru import logger
from fastapi.security import OAuth2PasswordBearer
from .models.user import User
from .db.database import SessionDep
from typing import Dict, Optional, Tuple


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]  # should be kept secre


def create_access_token(
    subject: Dict[str, str, int],  # type: ignore
    expire_delta: Optional[int] = None,  # type: ignore
) -> str:
    if expire_delta is not None:
        expires_delta = datetime.utcnow() + expire_delta  # type: ignore
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    logger.debug(f"subject:{subject}")
    to_encode = {
        "exp": expires_delta,
        "username": subject["username"],
        "email": subject["email"],
        "user_id": subject["user_id"],
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: dict[str, str, int], expire_delta: int = None) -> str:  # type: ignore
    if expire_delta is not None:
        expire_delta = datetime.utcnow() + expire_delta  # type: ignore
    else:
        expire_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire_delta,
        "username": subject["username"],
        "email": subject["email"],
        "user_id": subject["user_id"],
    }
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


outh_2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def verify_token(token: str, session: SessionDep) -> Tuple[User, bool] | None:  # type: ignore
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"decoded_token:{decoded_token}")
        logger.debug(decoded_token.get("user_id"))
        user = session.get(User, decoded_token.get("user_id", None))
        logger.debug(f"user:{user}")
        if not user:
            return user, False  # type: ignore
        return user, True
    except Exception as e:
        logger.error(f"error:{e}")
