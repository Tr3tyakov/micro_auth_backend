from sqlalchemy import Integer, Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class ArticleModel(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, name='Наименование')
    description = Column(String, name='Описание')
    date_created = Column(DateTime(timezone=True), nullable=False, name='Дата создания')
    date_edited = Column(DateTime(timezone=True), nullable=True, default=None, name='Дата редактирования')
    headline_id = Column(Integer, ForeignKey('headline.id'))

    def __str__(self):
        return f"{self.id}{self.name}"
