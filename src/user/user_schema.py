from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    age: Optional[int] = None
    city: Optional[str] = None
    phone: Optional[str] = None


class ResponseUser(User):
    id: int
    date_last_actions: Optional[datetime] = None
    date_register: datetime

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date_last_actions = self.formate_time(kwargs.get('date_last_actions'))
        self.date_register = self.formate_time(kwargs.get('date_register'))

    def formate_time(self, date):
        if date:
            return date.strftime("%d.%m.%Y %H:%m")
        return None


class ResetPassword(BaseModel):
    new_password: str
