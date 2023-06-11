import graphene

from database import async_session_maker
from src.user.graphql.interfaces.user_interfaces import User
from src.user.user_model import UserModel
from src.user.user_schema import ResponseUser
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

class Query(graphene.ObjectType):
    users = graphene.Field(graphene.List(User))

    async def resolve_users(self, info):
        async with async_session_maker() as session:
            result = await session.execute(select(UserModel))
            users = result.all()
            serializer = [ResponseUser(**item[0].__dict__) for item in users]
            json = jsonable_encoder(serializer)

            return json
