from typing import Optional, List, Any

from pydantic import BaseModel
from datetime import datetime

from src.images.image_schema import ImageResponse


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    age: Optional[int] = None
    city: Optional[str] = None
    phone: Optional[str] = None


class FullUser(User):
    password: str


class ResponseUser(User):
    id: int
    date_last_actions: Optional[datetime] = None
    date_register: datetime
    images: Optional[List[ImageResponse]] = []

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime("%d.%m.%Y %H:%M")
        }


class UpdateUser(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class ResetPassword(BaseModel):
    new_password: str
