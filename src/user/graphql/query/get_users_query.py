import graphene
from fastapi import HTTPException
from graphql import GraphQLError
from jose import ExpiredSignatureError, jwt
from sqlalchemy.orm import selectinload
from starlette import status

from database import async_session_maker
from src.user.graphql.interfaces.user_interfaces import User
from src.user.graphql.services.token_service import extract_user_from_token
from src.user.user_model import UserModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select


class GetUsersQuery(graphene.ObjectType):
    users = graphene.List(User)

    async def resolve_users(self, info):
        async with async_session_maker() as session:
            query = select(UserModel).options(selectinload(UserModel.images))
            result = await session.execute(query)
            users = result.all()
            serializer = [jsonable_encoder(item[0]) for item in users]
            return serializer
