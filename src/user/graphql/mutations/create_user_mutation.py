import os
from datetime import datetime

import graphene

from database import async_session_maker
from src.auth.mixins.tokens_mixin import TokenMixin
from src.smtp.smtp_service import SMTPService
from src.user.mixins.user_mixin import UserMixin
from src.user.user_model import UserModel
from sqlalchemy import select

from src.user.user_schema import FullUser, ResponseUser

CONFIRM_URL = os.getenv('CONFIRM_URL')
class CreateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        age = graphene.Int()
        city = graphene.String()
        phone = graphene.String()
        avatar = graphene.String()

    message = graphene.String()

    async def mutate(self, info, **kwargs):
        async with async_session_maker() as session:
            email = kwargs.get("email")
            phone = kwargs.get('phone')

            query = select(UserModel).where(UserModel.email == email, UserModel.phone == phone)
            result = await session.execute(query)
            users = result.all()
            if len(users) > 0:
                return CreateUserMutation(message='Данный пользователь уже существует')

            user_mixin = UserMixin(session=session)
            new_user = await user_mixin._create_user(FullUser(**kwargs))

            token_mixin = TokenMixin()
            hashed_user_data = token_mixin.create_access_token(user=ResponseUser(**new_user.__dict__))

            confirm_url = CONFIRM_URL + hashed_user_data['access_token']

            await SMTPService.send_message(email=new_user.email,
                                           subject='Подтверждение почты',
                                           mime_text=f'Ссылка для подтверждения почты {confirm_url}',
                                           session=session)

            return CreateUserMutation(message='Вам на почту отправлено письмо с подтверждением почты')

