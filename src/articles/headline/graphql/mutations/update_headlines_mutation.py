import graphene
from fastapi import HTTPException
from graphql import GraphQLError

from database import async_session_maker
from src.articles.headline.graphql.interfaces.headlines_interfaces import Headline
from src.articles.headline.graphql.services.services import Translater
from src.articles.headline.headline_service import HeadlineService
from src.user.graphql.services.token_service import extract_user_from_token


class UpdateHeadlinesMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        headline_id = graphene.Int()

    message = graphene.String()
    headline = graphene.Field(Headline)

    async def mutate(self, info, headline_id, **kwargs):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')
            print(headline_id, kwargs)
            updated_headline = await HeadlineService(session=session).update_headline(request=kwargs,
                                                                                      id=headline_id)
            return UpdateHeadlinesMutation(headline=updated_headline)
