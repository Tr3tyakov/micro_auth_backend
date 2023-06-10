from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select

from src.auth.mixins.depends_mixin import DependsMixin
from src.user.mixins.hash_mixin import HashMixin
from src.user.mixins.user_mixin import UserMixin
from src.user.user_model import UserModel


class CheckUserMixin(DependsMixin, HashMixin):
    async def _check_user(self, email, phone=None):
        is_phone_exsist = False
        is_email_exsist = False

        if phone:
            query = select(UserModel).where(UserModel.phone == phone)
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                is_phone_exsist = True

        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            is_email_exsist = True

        return {"is_phone_exsist": is_phone_exsist, "is_email_exsist": is_email_exsist}

    async def _check_password(self, email, password):
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            verify_result = await self._verify_password(password=password, hashed_password=user.password)
            if not verify_result:
                raise HTTPException(detail='Неправильный пароль', status_code=401)

        if not user.is_confirmed:
            raise HTTPException(detail='Доступ запрещен', status_code=status.HTTP_200_OK)

        user.date_last_actions = datetime.utcnow()
        await self.session.commit()
        return user
