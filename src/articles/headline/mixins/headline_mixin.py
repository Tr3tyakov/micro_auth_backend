from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from src.articles.headline.headline_model import HeadlineModel
from src.auth.mixins.depends_mixin import DependsMixin


class HeadlineMixin(DependsMixin):

    async def _get_headline(self, id: int):
        query = select(HeadlineModel).where(HeadlineModel.id == id).options(selectinload(HeadlineModel.articles))
        result = await self.session.execute(query)
        headline = result.scalar_one_or_none()

        if headline:
            return jsonable_encoder(headline)
        raise HTTPException(detail='Данного заголовка не существует', status_code=status.HTTP_400_BAD_REQUEST)
