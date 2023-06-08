from src.user.user_schema import User


class RegisterUser(User):
    password: str


class AuthUser:
    email: str
    password: str
