from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreatePost(BaseModel):

    user: Optional[int]
    title: str
    body : Optional[str]

class ReadPosts(BaseModel):
    id: int
    date: datetime
    user_id: Optional[int]
    title: str
    body: Optional[str]

class UpdatePost(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
