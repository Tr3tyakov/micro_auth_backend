from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    email: str
    username: str
    lastname: str
    age: Optional[int] = None
    city: Optional[int] = None


class CreateUser(User):
    pass


class ChangeUser(User):
    pass


class DeleteUser(User):
    pass


class RequestUser(User):
    password: str


class ResponseUser(User):
    id: int
    date_register: datetime
    last_authorization: datetime
