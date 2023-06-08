from sqlalchemy import Integer, Column, String, DateTime

from database import Base


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, name="Почта")
    first_name = Column(String, nullable=False, name="Имя")
    last_name = Column(String, nullable=False, name='Фамилия')
    age = Column(Integer, nullable=True, default=None, name='Лет')
    password = Column(String, nullable=False, name="Пароль")
    city = Column(String, nullable=True, default=None, name='Город')
    date_register = Column(DateTime, timezone=True, nullable=False, name='Дата регистрации')
    last_authorization = Column(DateTime, timezone=True, nullable=True, default=None, name='Дата последней авторизации')

    # google_token
    # apple_token



    def __str__(self):
        return f"{self.first_name}{self.last_name}"
