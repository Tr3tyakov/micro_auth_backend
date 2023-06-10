import random
import smtplib
import os
import string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException, status, Depends, Response

from sqlalchemy import select, update
from sqlalchemy.engine import create
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from src.auth.mixins.check_mixins import CheckUserMixin
from src.auth.mixins.depends_mixin import DependsMixin
from src.smtp.smtp_model import SMTPModel
from src.user.mixins.hash_mixin import HashMixin


class SMTPService(CheckUserMixin, DependsMixin):
    async def get_information(self):
        query = select(SMTPModel).where(SMTPModel.id == 1)
        result = await self.session.execute(query)
        smtp_information = result.scalar_one_or_none()

        if smtp_information is None:
            raise HTTPException(detail='SMTP информация отсутствует', status_code=status.HTTP_404_NOT_FOUND)

        return smtp_information

    async def set_information(self, request):
        try:
            information = await self.get_information()
        except HTTPException:
            new_information = SMTPModel(**request.dict())
            self.session.add(new_information)
            await self.session.commit()
            return new_information

        query = update(SMTPModel).where(SMTPModel.id == 1).values(**request.dict())
        await self.session.execute(query)
        await self.session.commit()
        await self.session.refresh(information)

        return information

    @staticmethod
    async def send_message(email, subject, mime_text, session: AsyncSession):
        query = select(SMTPModel).where(SMTPModel.id == 1)
        result = await session.execute(query)
        smtp = result.scalar_one_or_none()

        if smtp is None:
            raise HTTPException(detail='SMTP информация отсутствует', status_code=status.HTTP_404_NOT_FOUND)

        email_address = smtp.email_address
        email_login = smtp.email_login
        email_password = smtp.email_password
        smtp_address = smtp.smtp_address
        smtp_port = smtp.smtp_port

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = email_address
        msg["To"] = email

        msg.attach(MIMEText(mime_text))

        s = smtplib.SMTP(smtp_address, smtp_port)
        s.starttls()
        s.login(email_login, email_password)
        s.sendmail(email_address, [email], msg.as_string())
        s.quit()
