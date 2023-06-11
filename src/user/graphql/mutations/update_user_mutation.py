import os

import graphene

from database import async_session_maker
from sqlalchemy import update

from src.user.user_model import UserModel

CONFIRM_URL = os.getenv('CONFIRM_URL')


class UpdateUserMutation(graphene.Mutation):
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
            print(info)
            query = update(UserModel).where(UserModel.email == email)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user is None:
                return UpdateUserMutation(message='Данный пользователь не существует')

            query = update(UserModel).where(UserModel.email == email).values(**kwargs)
            await session.execute(query)
            await session.commit()
            await session.refresh(user)

            return UpdateUserMutation(message='FUCK')


class myMutation(graphene.ObjectType):
    user = UpdateUserMutation.Field()
