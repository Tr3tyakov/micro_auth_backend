from fastapi import APIRouter, Depends, UploadFile, Form, File

from src.images.image_schema import CreateImage
from src.images.image_service import ImageService
from src.user.dependens.auth_guard import authenticate
from src.user.user_schema import ResponseUser

router = APIRouter()


@router.post('/upload_image')
async def upload_image(user_id: int = Form(...), image: UploadFile = File(...), service: ImageService = Depends(),
                       user: ResponseUser = Depends(authenticate)):
    return await service.save(user_id=user_id, image=image)


@router.delete('/delete_image/{file_id}/')
async def delete_image(file_id: int, service: ImageService = Depends(), user: ResponseUser = Depends(authenticate)):
    return await service.delete(file_id=file_id)
