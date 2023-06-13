import os

from datetime import datetime
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, ExpiredSignatureError
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database import get_session
from config import load_dotenv
from src.user.user_model import UserModel


load_dotenv()

security = HTTPBearer()

ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security),
                       session: AsyncSession = Depends(get_session)):
    try:
        decoded_token = check_token(credentials.credentials)
    except HTTPException as exec:
        raise exec
    user = decoded_token['user']

    """Обновляем поле, date_last_actions при выполнении пользователем конкретного действия"""
    query = update(UserModel).where(UserModel.email == user['email']).values(
        date_last_actions=datetime.utcnow())
    await session.execute(query)
    await session.commit()

    """Получаем обновленного пользователя"""
    query = select(UserModel).where(UserModel.id == user['id']).options(selectinload(UserModel.images))
    result = await session.execute(query)
    updated_user = result.scalar_one_or_none()

    if updated_user is None:
        raise HTTPException(detail='Данный пользователь не зарегистрирован в сервисе',
                            status_code=status.HTTP_403_FORBIDDEN)

    return jsonable_encoder(updated_user)


def check_token(token):
    """Проверяем правильность/целостность токена"""
    try:
        return jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
