from sqlalchemy import Integer, Column, String, DateTime

from database import Base


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, name="Почта")
    first_name = Column(String(15), nullable=False, name="Имя")
    last_name = Column(String(20), nullable=False, name='Фамилия')
    age = Column(Integer, nullable=True, default=None, name='Лет')
    password = Column(String(20), nullable=False, name="Пароль")
    city = Column(String, nullable=True, default=None, name='Город')
    date_register = Column(DateTime(timezone=True), nullable=False, name='Дата регистрации')
    last_authorization = Column(DateTime(timezone=True), nullable=True, default=None, name='Дата последней авторизации')
    phone = Column(String(12), default=None, nullable=True, name='Телефон', )
    avatar = Column(String, default=None, nullable=True, name='Аватар')

    # google_token
    # apple_token

    def __str__(self):
        return f"{self.first_name}{self.last_name}"
