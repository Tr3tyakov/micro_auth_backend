from fastapi import HTTPException
from sqlalchemy import select

from src.auth.mixins.depends_mixin import DependsMixin
from src.user.user_model import UserModel


class CheckMixin(DependsMixin):
    async def _check(self, email, phone):
        if phone:
            query = select(UserModel).where(UserModel.phone == phone)
            result = await self.session.execute(query)
            users = result.scalar_one_or_none()
            if users:
                raise HTTPException(detail='Данный телефон уже зарегистрирован в сервисе', status_code=403)

        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        users = result.scalar_one_or_none()
        print(users)
        if users:
            raise HTTPException(detail="Данный Email уже зарегистрирован в сервисе", status_code=403)
