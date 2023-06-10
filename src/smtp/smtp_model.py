from sqlalchemy import Column, String, Integer

from database import Base


class SMTPModel(Base):
    __tablename__ = 'smtp'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, name='Адрес почты')
    email_password = Column(String, name='Пароль почты')
    email_login = Column(String, name='Логин почты')
    smtp_address = Column(String, name='SMTP адрес')
    smtp_port = Column(String, name='SMTP порт')

    def __str__(self):
        return f"smtp {self.smtp_address}"

# nasutkicalendar@yandex.ru
# smtp.yandex.ru
# 465
# ?
