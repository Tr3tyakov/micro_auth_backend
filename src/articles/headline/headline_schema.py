from datetime import datetime

from pydantic import BaseModel
from typing import List

from src.articles.article.article_schema import ArticleResponse


class HeadlineBase(BaseModel):
    name: str


class HeadlineResponse(HeadlineBase):
    id: int
    date_created: datetime
    date_edited: datetime
    articles: List[ArticleResponse]

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.strftime("%d.%m.%Y %H:%M")
        }


class HeadlineCreate(HeadlineBase):
    pass
