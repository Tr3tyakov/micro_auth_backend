import graphene
from database import async_session_maker
from src.articles.headline.graphql.interfaces.headlines_interfaces import Headline
from src.articles.headline.headline_service import HeadlineService


class GetHeadlinesQuery(graphene.ObjectType):
    headlines = graphene.List(Headline)
    headline = graphene.Field(Headline, headline_id=graphene.Int(default_value=None))

    async def resolve_headlines(self, info):
        async with async_session_maker() as session:
            headline_service = HeadlineService(session=session)
            return await headline_service.get_all_headlines()

    async def resolve_headline(self, info, headline_id):
        async with async_session_maker() as session:
            headline_service = HeadlineService(session=session)
            return await headline_service.get_headline(id=headline_id)
