import graphene

from fastapi import HTTPException
from graphql import GraphQLError
from database import async_session_maker
from src.articles.article.article_service import ArticleService
from src.articles.article.graphql.interfaces.article_interfaces import Article
from src.articles.headline.graphql.services.services import Translater
from src.user.graphql.services.token_service import extract_user_from_token


class CreateArticleMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        headline_id = graphene.Int()

    article = graphene.Field(Article)

    async def mutate(self, info, **kwargs):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')
            try:
                new_article = await ArticleService(session=session).create_article(request=Translater(**kwargs))
            except HTTPException:
                raise GraphQLError(message="Данного заголовка не существует")
            return CreateArticleMutation(article=new_article)
