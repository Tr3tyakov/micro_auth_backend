from fastapi import HTTPException
from fastapi.openapi.models import Response

from src.auth.mixins.check_mixins import CheckMixin
from src.user.mixins.user_mixin import UserMixin


class AuthService(CheckMixin, UserMixin):
    async def registration(self, request):
        try:
            await self._check(email=request.email, phone=request.phone)
        except HTTPException as exec:
            raise exec

        user = await self._create_user(request=request)
        return user

    def authorization(self, request):
        pass

    def google_authorization(self):
        pass

    def vk_authorization(self):
        pass

    def github_authorization(self):
        pass

    def apple_authorization(self):
        pass
