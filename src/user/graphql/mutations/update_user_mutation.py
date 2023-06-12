import os

import graphene
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from graphql import GraphQLError
from sqlalchemy.sql.functions import user

from database import async_session_maker
from sqlalchemy import update, select

from src.user.graphql.interfaces.user_interfaces import User
from src.user.graphql.services.token_service import extract_user_from_token
from src.user.mixins.hash_mixin import HashMixin
from src.user.user_model import UserModel
from src.user.user_schema import UpdateUser

CONFIRM_URL = os.getenv('CONFIRM_URL')


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        age = graphene.Int()
        city = graphene.String()
        phone = graphene.String()

    message = graphene.String()
    user = graphene.Field(User)

    async def mutate(self, info, **kwargs):
        async with async_session_maker() as session:
            try:
                extracted_user = extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')

            query = update(UserModel).where(UserModel.email == extracted_user['email']).values(
                email=kwargs.get('email', extracted_user['email']),
                first_name=kwargs.get('email', extracted_user['first_name']),
                last_name=kwargs.get('email', extracted_user['last_name']),
                age=kwargs.get('age', extracted_user['age']),
                city=kwargs.get('city', extracted_user['city']),
                phone=kwargs.get('phone', extracted_user['phone']),
            )
            await session.execute(query)
            await session.commit()

            query = select(UserModel).where(UserModel.id == extracted_user['id'])
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            return UpdateUserMutation(user=jsonable_encoder(user))


class myMutation(graphene.ObjectType):
    user = UpdateUserMutation.Field()
