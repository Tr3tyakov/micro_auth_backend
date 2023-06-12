import graphene
from fastapi import HTTPException
from graphql import GraphQLError
from sqlalchemy.orm import selectinload

from database import async_session_maker
from src.user.graphql.interfaces.user_interfaces import User
from src.user.graphql.services.token_service import extract_user_from_token
from src.user.user_model import UserModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select


class GetUserInfoQuery(graphene.ObjectType):
    user = graphene.Field(User, user_id=graphene.Int(default_value=None))

    async def resolve_user(self, info, user_id):
        async with async_session_maker() as session:
            try:
                user = extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')

            if user_id is None:
                query = select(UserModel).where(UserModel.id == user['id']).options(
                    selectinload(UserModel.images))
            else:
                query = select(UserModel).where(UserModel.id == user_id).options(selectinload(UserModel.images))

            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return jsonable_encoder(user)
