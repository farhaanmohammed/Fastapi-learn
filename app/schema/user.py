from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password:str
    first_name: Optional[str]
    last_name: Optional[str]

class UserRead(BaseModel):
    id:int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]





