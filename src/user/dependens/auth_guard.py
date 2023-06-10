import os
from datetime import datetime

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, ExpiredSignatureError
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from time import time
from database import get_session
from config import load_dotenv
from src.user.user_model import UserModel
from src.user.user_schema import ResponseUser

load_dotenv()

security = HTTPBearer()

ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security),
                       session: AsyncSession = Depends(get_session)):
    token = credentials.credentials
    try:
        """Проверяем правильность/целостность токена"""
        decoded_token = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = decoded_token['user']

    """Обновляем поле, last_authorization при выполнении пользователем конкретного действия"""
    query = update(UserModel).where(UserModel.email == user['email']).values(
        last_authorization=datetime.utcnow())
    await session.execute(query)
    await session.commit()

    """Получаем обновленного пользователя и сериализуем его"""
    query = select(UserModel).where(UserModel.id == user['id'])
    result = await session.execute(query)
    updated_user = result.scalar_one_or_none()
    serializer = ResponseUser(**updated_user.__dict__)

    return serializer
