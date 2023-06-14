import graphene

from fastapi import HTTPException
from graphql import GraphQLError
from database import async_session_maker
from src.articles.article.article_service import ArticleService
from src.articles.article.graphql.interfaces.article_interfaces import Article
from src.user.graphql.services.token_service import extract_user_from_token


class DeleteArticleMutation(graphene.Mutation):
    class Arguments:
        article_id = graphene.Int()

    message = graphene.String()

    async def mutate(self, info, article_id):
        async with async_session_maker() as session:
            try:
                extract_user_from_token(info)
            except HTTPException:
                raise GraphQLError(message='Token is invalid')
            try:
                await ArticleService(session=session).delete_article(article_id=article_id)
            except HTTPException:
                raise GraphQLError(message='Данной записи не существует')
            return DeleteArticleMutation(message='Запись успешно удалена')
