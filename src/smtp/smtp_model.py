from sqlalchemy import Column, String, Integer

from database import Base


class SMTPModel(Base):
    __tablename__ = 'smtp'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, name='Адрес почты')
    smtp_address = Column(String, name='SMTP адрес')
    smtp_port = Column(String, name='SMTP порт')
    email_password = Column(String, name='Пароль почты')

    def __str__(self):
        return f"smtp {self.smtp_address}"
