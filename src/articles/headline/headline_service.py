from datetime import datetime

from fastapi import HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.articles.headline.headline_model import HeadlineModel
from src.articles.headline.mixins.headline_mixin import HeadlineMixin


class HeadlineService(HeadlineMixin):
    async def create_headline(self, request):
        datenow = datetime.utcnow()
        headline = HeadlineModel(
            name=request.name,
            date_created=datenow,
            date_edited=datenow,
        )
        self.session.add(headline)
        await self.session.commit()
        return jsonable_encoder(headline)

    async def get_all_headlines(self):
        query = select(HeadlineModel).options(selectinload(HeadlineModel.articles))
        result = await self.session.execute(query)
        headlines = result.all()
        return [jsonable_encoder(item[0]) for item in headlines]

    async def get_headline(self, id):
        try:
            return await self._get_headline(id=id)
        except HTTPException as exec:
            raise exec

    async def update_headline(self, id, request):
        try:
            headline = await self._get_headline(id=id)
        except HTTPException as exec:
            raise exec

        query = update(HeadlineModel).where(HeadlineModel.id == id).options(HeadlineModel.articles).values(
            name=request.get('name', headline['name']),
            date_edited=datetime.utcnow()
        )
        await self.session.execute(query)
        await self.session.commit()
        updated_headline = await self._get_headline(id=id)
        return updated_headline

    async def delete_headline(self, id):
        try:
            await self._get_headline(id=id)
        except HTTPException as exec:
            raise exec

        query = delete(HeadlineModel).where(HeadlineModel.id == id)
        await self.session.execute(query)
        await self.session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
