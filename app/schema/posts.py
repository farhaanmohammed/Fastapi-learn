from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreatePost(BaseModel):
    id: int
    user: Optional[int]
    title: str
    body : Optional[str]

class Posts(CreatePost):
    date: datetime