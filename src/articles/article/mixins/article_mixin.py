from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.articles.article.article_model import ArticleModel
from src.auth.mixins.depends_mixin import DependsMixin


class ArticleMixin(DependsMixin):

    async def _get_articles(self, headline_id=None):
        if headline_id is None:
            query = select(ArticleModel)
        else:
            query = select(ArticleModel).where(ArticleModel.headline_id == headline_id)

        result = await self.session.execute(query)
        articles = result.all()
        return [jsonable_encoder(item[0]) for item in articles]

    async def _get_article(self, article_id):
        query = select(ArticleModel).where(ArticleModel.id == article_id)

        result = await self.session.execute(query)
        article = result.scalar_one_or_none()
        if article:
            return jsonable_encoder(article)
        raise HTTPException(detail='Данной записи не существует', status_code=status.HTTP_404_NOT_FOUND)
