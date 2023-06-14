import graphene

from fastapi import HTTPException
from graphql import GraphQLError
from database import async_session_maker
from src.articles.article.article_service import ArticleService
from src.articles.article.graphql.interfaces.article_interfaces import Article
from src.articles.headline.graphql.services.services import Translater
from src.user.graphql.services.token_service import extract_user_from_token


class UpdateArticleMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        article_id = graphene.Int()
        headline_id = graphene.Int()

    article = graphene.Field(Article, article_id=graphene.Int())

    async def mutate(self, info, article_id, **kwargs):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')
            try:
                updated_article = await ArticleService(session=session).update_article(request=kwargs,
                                                                                       article_id=article_id)
            except HTTPException:
                raise GraphQLError(message='Данной записи не существует')
            return UpdateArticleMutation(article=updated_article)
