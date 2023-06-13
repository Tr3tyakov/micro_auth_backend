import graphene
from sqlalchemy.orm import selectinload
from database import async_session_maker
from src.user.graphql.interfaces.user_interfaces import User
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
