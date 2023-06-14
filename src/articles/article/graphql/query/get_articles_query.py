import graphene
from fastapi import HTTPException
from graphql import GraphQLError

from database import async_session_maker
from src.articles.article.article_service import ArticleService
from src.articles.article.graphql.interfaces.article_interfaces import Article
from src.articles.headline.graphql.interfaces.headlines_interfaces import Headline
from src.user.graphql.services.token_service import extract_user_from_token


class GetArticlesQuery(graphene.ObjectType):
    headline_articles = graphene.List(Article, headline_id=graphene.Int())
    all_articles = graphene.List(Article)
    article = graphene.Field(Article, article_id=graphene.Int())

    async def resolve_article(self, info, article_id):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')
            try:
                test = await ArticleService(session=session).get_article_by_id(article_id=article_id)
                print(test, 'test')
                return test
            except HTTPException:
                raise GraphQLError(message='Данной записи не существует')

    async def resolve_all_articles(self, info):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')

            return await ArticleService(session=session).get_all_articles()

    async def resolve_headline_articles(self, info, headline_id):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')
            return await ArticleService(session=session).get_headline_articles(headline_id=headline_id)
