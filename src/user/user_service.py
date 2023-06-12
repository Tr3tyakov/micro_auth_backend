import json
import string
import random

from fastapi.encoders import jsonable_encoder
from jose import ExpiredSignatureError
from sqlalchemy import delete, select, update
from fastapi import HTTPException, status, Response
from sqlalchemy.orm import selectinload
from starlette.responses import JSONResponse

from src.auth.mixins.check_mixins import CheckUserMixin
from src.smtp.smtp_service import SMTPService

from src.user.mixins.user_mixin import UserMixin
from src.user.user_model import UserModel
from src.user.user_schema import ResponseUser


class UserService(UserMixin, CheckUserMixin):
    serializer_class = ResponseUser

    async def get_all_user(self):
        result = await self.session.execute(select(UserModel).options(selectinload(UserModel.images)))
        rows = result.all()

        return [jsonable_encoder(item[0]) for item in rows]

    async def delete_user(self, user):
        query = delete(UserModel).where(UserModel.id == user["id"])
        await self.session.execute(query)
        await self.session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def update_info(self, request, user):
        query = update(UserModel).where(UserModel.id == user['id']).values(
            email=request.get('email', user["email"]),
            first_name=request.get('email', user["first_name"]),
            last_name=request.get('email', user["last_name"]),
            age=request.get('age', user["age"]),
            city=request.get('city', user["city"]),
            phone=request.get('phone', user["phone"]),
        )
        await self.session.execute(query)
        await self.session.commit()

        query = select(UserModel).where(UserModel.id == user['id']).options(selectinload(UserModel.images))
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return jsonable_encoder(user)

    async def reset_password(self, request, user):
        new_password = request.get('new_password')

        hash_password = self._hash_password(new_password)
        query = update(UserModel).where(UserModel.id == user["id"]).values(password=hash_password)
        await self.session.execute(query)
        await self.session.commit()
        return JSONResponse(content={'detail': 'Пароль успешно обновлен'}, status_code=status.HTTP_200_OK)

    async def forgot_password(self, request):
        email = request.get('email')

        if email is None:
            raise HTTPException(detail='Поле email - обязательное поле', status_code=status.HTTP_403_FORBIDDEN)

        result = await self._check_user(email=email)
        if not result['is_email_exsist']:
            raise HTTPException(detail='Данный пользователь не зарегистрирован в сервисе',
                                status_code=status.HTTP_400_BAD_REQUEST)

        new_password = generate_new_password()
        hash_password = self._hash_password(new_password)

        query = update(UserModel).where(UserModel.email == email).values(password=hash_password)
        await self.session.execute(query)
        await self.session.commit()

        await SMTPService.send_message(email=email, subject='Новый пароль',
                                       mime_text=f'Добрый день, Ваш новый пароль:\n{new_password}',
                                       session=self.session)

        return JSONResponse(content=({'detail': 'Вам на почту отправлено письмо с новым паролем'}),
                            status_code=status.HTTP_200_OK)


def generate_new_password(length=10):
    items = string.ascii_letters + string.digits + '@#$%&*?!'
    new_password = ''
    for _ in range(length):
        new_password += random.choice(items)

    return new_password
