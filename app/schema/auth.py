from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    access_token: str
    refresh_token: str


class Login(BaseModel):
    username: str
    password: str
