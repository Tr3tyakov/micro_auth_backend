import os

from fastapi.encoders import jsonable_encoder
from jose import jwt, ExpiredSignatureError
from fastapi import HTTPException,status
from sqlalchemy import update
from starlette.responses import JSONResponse
from src.auth.mixins.check_mixins import CheckUserMixin
from src.auth.mixins.tokens_mixin import TokenMixin
from src.smtp.smtp_service import SMTPService
from src.user.mixins.user_mixin import UserMixin
from src.user.user_model import UserModel

CONFIRM_URL = os.getenv('CONFIRM_URL')

class AuthService(CheckUserMixin, TokenMixin, UserMixin):
    async def registration(self, request):
        '''Проверяем данные пользователя'''
        result = await self._check_user(email=request.email, phone=request.phone)

        if result['is_phone_exsist']:
            raise HTTPException(detail='Данный телефон уже зарегистрирован в сервисе', status_code=403)

        if result['is_email_exsist']:
            raise HTTPException(detail="Данный Email уже зарегистрирован в сервисе", status_code=403)

        user = await self._create_user(request=request)
        hashed_user_data = self.create_access_token(user=jsonable_encoder(user))
        confirm_url = CONFIRM_URL + hashed_user_data['access_token']

        await SMTPService.send_message(email=user.email,
                                       subject='Подтверждение почты',
                                       mime_text=f'Ссылка для подтверждения почты {confirm_url}',
                                       session=self.session)

        return JSONResponse(content={"detail": "Вам на почту отправлена ссылка для подтверждения почты"},
                            status_code=200)

    async def authorization(self, request):
        email = request.email
        password = request.password

        '''Проверяем, что пользователь существует в базе'''
        result = await self._check_user(email=email)
        if not result['is_email_exsist']:
            raise HTTPException(detail="Данный Email не зарегистрирован в сервисе", status_code=403)

        try:
            '''Проверяем правильность пароля'''
            user = await self._check_password(email=email, password=password)
        except HTTPException as exec:
            raise exec

        response_user = jsonable_encoder(user)
        tokens = self.create_access_token(user=response_user)

        return {"user": response_user, "tokens": tokens}

    async def confirm_email(self, user):
        try:
            user_data = self.decode_access_token(user)
        except ExpiredSignatureError as exec:
            raise exec
        except jwt.JWTError as jwt_exec:
            raise jwt_exec

        user_id = user_data['user']['id']

        query = update(UserModel).where(UserModel.id == user_id).values(is_confirmed=True)
        await self.session.execute(query)
        await self.session.commit()
        return JSONResponse('Почта успешно подтверждена', status_code=status.HTTP_200_OK)

