from pydantic import BaseModel
from src.user.user_schema import User, ResponseUser


class AuthUser(BaseModel):
    email: str
    password: str

class ResponsePartAuthTokens(BaseModel):
    access_token: str
    refresh_token: str

class ResponseAuthUser(BaseModel):
    user: ResponseUser
    tokens: ResponsePartAuthTokens


class RegisterUser(User):
    password: str
