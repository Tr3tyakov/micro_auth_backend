from sqlalchemy import Column, ForeignKey, Integer, DateTime

from database import Base


class LogsModel(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    datetime_open = Column(DateTime(timezone=True), nullable=False, name='Дата открытия')
    user_id = Column(ForeignKey('user.id'))
    headline_id = Column(ForeignKey('headline.id'))

    def __str__(self):
        return f"ID:{self.id}, date:{self.datetime_open}"
