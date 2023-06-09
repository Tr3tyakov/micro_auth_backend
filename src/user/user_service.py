from inspect import isclass

from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import Response
from sqlalchemy import delete, select
from fastapi import HTTPException, status

from src.user.mixins.serializer_mixin import SerializerMixin
from src.user.mixins.user_mixin import UserMixin
from src.user.user_model import UserModel
from src.user.user_schema import ResponseUser


class UserService(UserMixin, SerializerMixin):
    serializer_class = ResponseUser

    async def get_all_user(self):
        result = await self.session.execute(select(UserModel))
        rows = result.all()
        return self._get_serializer(rows)

    async def get_user(self, id):
        user = await self._get_user_by_id(id=id)
        if not user:
            raise HTTPException(detail="Данного пользователя не существует", status_code=status.HTTP_404_NOT_FOUND)
        return self._get_serializer(user)

    async def delete_user(self, id):
        user = await self._get_user_by_id(id=id)

        if not user:
            raise HTTPException(detail="Данного пользователя не существует", status_code=status.HTTP_404_NOT_FOUND)

        query = delete(UserModel).where(UserModel.id == id)
        await self.session.execute(query)
        await self.session.commit()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def reset_password(self, request):
        pass

    def forgot_password(self, request):
        pass

    def change_info(self, request):
        pass
