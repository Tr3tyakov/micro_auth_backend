import graphene
from fastapi import HTTPException
from graphql import GraphQLError

from database import async_session_maker
from src.articles.headline.graphql.interfaces.headlines_interfaces import Headline
from src.articles.headline.graphql.services.services import Translater
from src.articles.headline.headline_service import HeadlineService
from src.user.graphql.services.token_service import extract_user_from_token


class DeleteHeadlinesMutation(graphene.Mutation):
    class Arguments:
        headline_id = graphene.Int()

    message = graphene.String()

    async def mutate(self, info, headline_id):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')

            try:
                await HeadlineService(session=session).delete_headline(id=headline_id)
            except HTTPException:
                raise GraphQLError(message='Данного заголовка не существует')

            return DeleteHeadlinesMutation(message='Заголовок успешно удален')
