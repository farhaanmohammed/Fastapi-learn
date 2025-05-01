from fastapi import APIRouter,HTTPException
from sqlmodel import select
from ..models.user import User
from app.db.database import SessionDep
from ..schema.user import UserRead

router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/login",response_model=UserRead)
def login(username:str,password:str,session: SessionDep):
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    if not user or user.verify_password(password):
        raise HTTPException(status_code=400,detail="Invalid username or password")

    return user