from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from passlib.context import CryptContext
from .posts import Posts

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    hashed_password: str
    email: EmailStr
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    posts: list["Posts"] = Relationship(back_populates="user")

    def __init__(self, **kwargs):
        raw_password = kwargs.pop("hashed_password")
        super().__init__(**kwargs)
        if raw_password:
            self.hashed_password = pwd_context.hash(raw_password)

    def verify_password(self, plain_password: str) -> bool:
        """Check password matches the stored password of user"""
        return pwd_context.verify(plain_password, self.hashed_password)
