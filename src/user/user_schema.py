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



class ResetPassword(BaseModel):
    new_password: str