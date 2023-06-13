import os

from sqlalchemy import delete
from fastapi import UploadFile, status
from sqlalchemy import select
from starlette.responses import JSONResponse
from src.auth.mixins.depends_mixin import DependsMixin
from src.images.image_schema import ImageResponse
from src.images.image_model import ImageModel


class ImageService(DependsMixin):
    path = './src/static/uploaded_files/'

    async def __upload_file(self, file: UploadFile):
        with open(self.path + file.filename, 'wb') as uploaded_file:
            uploaded_file.write(await file.read())
            uploaded_file.close()
        return file.filename

    async def get(self, path: str):
        query = select(ImageModel).where(ImageModel.url == path)
        result = await self.session.execute(query)

        is_exsist = result.scalar_one_or_none()
        if is_exsist == None:
            return None
        return is_exsist

    async def save(self, user_id: int, image: UploadFile):
        filename = await self.__upload_file(image)
        path = f'/micro_alerts/static/{filename}'
        file_dict = {'url': path, 'user_id': user_id}
        new_url = ImageModel(**file_dict)
        self.session.add(new_url)
        await self.session.commit()
        await self.session.refresh(new_url)
        return new_url

    async def delete(self, file_id: int) -> status:
        query = select(ImageModel).where(ImageModel.id == file_id)

        result = await self.session.execute(query)
        image = result.scalar_one_or_none()

        if image is not None:
            filename = ImageResponse(**image.__dict__).url.split('/')[3]
            file_path = os.path.join(f"{self.path}", filename)

            if os.path.exists(file_path):
                os.remove(file_path)

        query = delete(ImageModel).where(ImageModel.id == file_id)
        await self.session.execute(query)
        await self.session.commit()
        return JSONResponse(content={"detail": "Файл успешно удален"}, status_code=status.HTTP_200_OK)
