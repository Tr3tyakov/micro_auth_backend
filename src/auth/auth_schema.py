from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel

from src.user.user_schema import User


class AuthUser(BaseModel):
    email: str
    password: str


class ResponsePartAuthUser(User):
    id: int
    last_authorization: datetime
    date_register: datetime

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_authorization = self.formate_time(kwargs.get('last_authorization'))
        self.date_register = self.formate_time(kwargs.get('date_register'))

    def formate_time(self, date):
        if date:
            return date.strftime("%d.%m.%Y %H:%m")
        return None


class ResponsePartAuthTokens(BaseModel):
    access_token: str
    refresh_token: str


class ResponseAuthUser(BaseModel):
    user: ResponsePartAuthUser
    tokens: ResponsePartAuthTokens


class RegisterUser(User):
    password: str
