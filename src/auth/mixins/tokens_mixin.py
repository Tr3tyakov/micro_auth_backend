from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, ExpiredSignatureError
from starlette import status

from src.auth.mixins.depends_mixin import DependsMixin
from config import load_dotenv
from src.user.user_schema import ResponseUser

load_dotenv()

import os


class TokenMixin(DependsMixin):
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
    REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

    def generate_tokens(self, user: dict, expires_delta=None):
        '''Если RefreshToken не требуется, вводим свое собственное время жизни токена'''
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
            refresh_expire = expire
        else:
            expire = self._get_expire(self.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_expire = self._get_expire(self.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = self._generate_token(user=user, key=self.ACCESS_SECRET_KEY, expire=expire)
        refresh_token = self._generate_token(user=user, key=self.REFRESH_SECRET_KEY, expire=refresh_expire)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def _get_expire(self, expire_minutes):
        return datetime.utcnow() + timedelta(minutes=int(expire_minutes))

    def decode_access_token(self, token):
        try:
            """Проверяем правильность/целостность токена"""
            return jwt.decode(token, self.ACCESS_SECRET_KEY, algorithms=[self.ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def decode_refresh_token(self, token):
        try:
            """Проверяем правильность/целостность токена"""
            return jwt.decode(token, self.REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def _generate_token(self, user, key, expire):
        user.pop('images', None)
        user.pop("password", None)
        to_encode = {"exp": expire, "user": user}
        return jwt.encode(to_encode, key, algorithm=self.ALGORITHM)
