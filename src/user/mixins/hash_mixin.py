import os

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SERCRET = os.getenv("SECRET")

class HashMixin:
    @staticmethod
    def _hash_password(password):
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(password, hashed_password):
        return pwd_context.verify(password, hashed_password)
