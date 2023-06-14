from fastapi import HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, update
from datetime import datetime
from src.articles.article.article_model import ArticleModel
from src.articles.article.mixins.article_mixin import ArticleMixin
from src.articles.headline.mixins.headline_mixin import HeadlineMixin


class ArticleService(ArticleMixin, HeadlineMixin):
    async def get_all_articles(self):
        return await self._get_articles()

    async def get_headline_articles(self, headline_id):
        return await self._get_articles(headline_id=headline_id)

    async def create_article(self, request):
        try:
            await self._get_headline(id=request.headline_id)
        except HTTPException as exec:
            raise exec

        new_article = ArticleModel(
            name=request.name,
            description=request.description,
            date_created=datetime.utcnow(),
            date_edited=datetime.utcnow(),
            headline_id=request.headline_id
        )

        self.session.add(new_article)
        await self.session.commit()
        await self.session.refresh(new_article)
        return jsonable_encoder(new_article)

    async def get_article_by_id(self, article_id):
        try:
            return await self._get_article(article_id=article_id)
        except HTTPException as exec:
            raise exec

    async def delete_article(self, article_id):
        try:
            await self._get_article(article_id=article_id)
        except HTTPException as exec:
            raise exec

        query = delete(ArticleModel).where(ArticleModel.id == article_id)
        await self.session.execute(query)
        await self.session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def update_article(self, request, article_id):
        try:
            article = await self._get_article(article_id=article_id)
        except HTTPException as exec:
            raise exec

        query = update(ArticleModel).where(ArticleModel.id == article_id).values(
            name=request.get('name', article['name']),
            description=request.get('description', article['description']),
            headline_id=request.get('headline_id', article['headline_id'])
        )
        await self.session.execute(query)
        await self.session.commit()
        updated_article = await self._get_article(article_id=article_id)
        return updated_article
