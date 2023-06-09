from sqlalchemy import select

from src.user.mixins.serializer_mixin import SerializerMixin
from src.user.user_model import UserModel
from src.auth.mixins.depends_mixin import DependsMixin
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserMixin(DependsMixin):

    async def _hash_password(self, password):
        return pwd_context.hash(password)

    async def _verify_password(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)

    async def _get_user_by_id(self, id):
        query = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        print(user)
        return user

    async def _create_user(self, request):
        hash_password = await self._hash_password(request.password)
        date_register = datetime.utcnow()
        user = UserModel(
            password=hash_password,
            phone=request.phone,
            email=request.email,
            age=request.age,
            city=request.city,
            last_name=request.last_name,
            first_name=request.first_name,
            date_register=date_register
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
