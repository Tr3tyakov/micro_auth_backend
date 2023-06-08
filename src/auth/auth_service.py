from datetime import timedelta, datetime

from jose import JWTError, jwt
from fastapi import HTTPException

from src.auth.auth_schema import ResponseAuthUser, ResponsePartAuthUser, ResponsePartAuthTokens
from src.auth.mixins.check_mixins import CheckMixin
from src.auth.mixins.tokens_mixin import TokenMixin


class AuthService(CheckMixin, TokenMixin):
    async def registration(self, request):
        '''Проверяем данные пользователя'''
        result = await self._check_user(email=request.email, phone=request.phone)

        if result['is_phone_exsist']:
            raise HTTPException(detail='Данный телефон уже зарегистрирован в сервисе', status_code=403)

        if result['is_email_exsist']:
            raise HTTPException(detail="Данный Email уже зарегистрирован в сервисе", status_code=403)

        user = await self._create_user(request=request)
        return user

    async def authorization(self, request):
        email = request.email
        password = request.password

        '''Проверяем, что пользователь существует в базе'''
        result = await self._check_user(email=email)
        if not result['is_email_exsist']:
            raise HTTPException(detail="Данный Email не зарегистрирован в сервисе", status_code=403)

        '''Проверяем правильность пароля'''
        try:
            user = await self._check_password(email=email, password=password)
        except HTTPException as exec:
            raise exec

        tokens = self.create_access_token(user_id=user.id)

        response_user = ResponsePartAuthUser(**user.__dict__)
        return {"user": response_user, "tokens": tokens}

    def google_authorization(self):
        pass
