from src.articles.article.article_model import ArticleModel
from sqlalchemy import Integer, Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base


class HeadlineModel(Base):
    __tablename__ = 'headline'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, name='Наименование заголовка')
    date_created = Column(DateTime(timezone=True), nullable=False, name='Дата создания')
    date_edited = Column(DateTime(timezone=True), nullable=True, default=None, name='Дата редактирования')
    articles = relationship('ArticleModel', cascade='all, delete')

    def __str__(self):
        return f"{self.id}{self.name}"
