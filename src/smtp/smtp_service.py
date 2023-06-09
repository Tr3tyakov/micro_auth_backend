import smtplib
import os

from email.mime.multipart import MIMEMultipart

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.engine import create

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

    async def send_message(self, email, response_message, subject):
        result = await self._check_user(email=email)
        if not result['is_email_exsist']:
            raise HTTPException(detail="Данный Email не зарегистрирован в сервисе", status_code=403)

        try:
            smtp_information = await self.get_information()
        except HTTPException as exec:
            raise exec

        print(smtp_information)
