import graphene
from fastapi import HTTPException
from graphql import GraphQLError

from database import async_session_maker
from src.articles.headline.graphql.interfaces.headlines_interfaces import Headline
from src.articles.headline.graphql.services.services import Translater
from src.articles.headline.headline_service import HeadlineService
from src.user.graphql.services.token_service import extract_user_from_token


class CreateHeadlinesMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    message = graphene.String()
    headline = graphene.Field(Headline)

    async def mutate(self, info, **kwargs):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')

            new_headline = await HeadlineService(session=session).create_headline(request=Translater(**kwargs))
            print(new_headline)
            return CreateHeadlinesMutation(headline=new_headline)
