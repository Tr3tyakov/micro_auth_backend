from datetime import datetime
from pydantic import BaseModel


class ArticleBase(BaseModel):
    name: str
    description: str


class ArticleResponse(ArticleBase):
    id: int
    date_created: datetime
    date_edited: datetime
    headline_id: int

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime("%d.%m.%Y %H:%M")
        }


class ArticleCreate(ArticleBase):
    headline_id: int
