from src.user.user_model import UserModel
from src.auth.mixins.depends_mixin import DependsMixin
from passlib.context import CryptContext
from datetime import datetime


class UserMixin(DependsMixin):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def _hash_password(self, password):
        return self.pwd_context.hash(password)

    async def _verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    async def _create_user(self, request):
        hash_password = await self._hash_password(request.password)
        user = UserModel(
            password=hash_password,
            phone=request.phone,
            email=request.email,
            age=request.age,
            city=request.city,
            last_name=request.last_name,
            first_name=request.first_name,
            date_register=datetime.utcnow()
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
