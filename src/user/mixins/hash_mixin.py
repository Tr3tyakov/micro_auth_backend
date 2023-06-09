from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class HashMixin:
    async def _hash_password(self, password):
        return pwd_context.hash(password)

    async def _verify_password(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)
