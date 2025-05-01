from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password:str
    first_name: Optional[str] = Field(default=None,alias="firstname")
    last_name: Optional[str] = Field(default=None,alias="lastname")

class UserRead(BaseModel):
    id:int
    username: str
    email: EmailStr
    first_name: Optional[str] = Field(default=None,alias="firstname")
    last_name: Optional[str] = Field(default=None,alias="lastname")



