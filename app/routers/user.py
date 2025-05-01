from fastapi import APIRouter,HTTPException
from sqlmodel import  select
from app.models.user import User
from app.db.database import SessionDep
from app.schema.user import UserRead,UserCreate
import logging


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user",tags=["Users"])

@router.post("/register",response_model=UserRead)
def create_user(user_create:UserCreate,session: SessionDep):
    print(f"firstname:{user_create.first_name},lastname:{user_create.last_name}")
    statement = select(User).where(User.username == user_create.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User with username already exists")

    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=user_create.password,
        first_name= user_create.first_name,
        last_name=user_create.last_name
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/",response_model=list[UserRead],response_model_by_alias=True)
def read_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users