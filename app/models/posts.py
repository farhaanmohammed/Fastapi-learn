from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from .user import User


class Posts(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, unique=True)
    date: datetime = Field(nullable=False)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="posts")
    title: str = Field(nullable=False, max_length=100)
    body: str | None = Field(default=None, nullable=True)
