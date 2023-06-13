from typing import List

from fastapi import Depends, APIRouter

from src.articles.headline.headline_schema import HeadlineResponse, HeadlineCreate
from src.articles.headline.headline_service import HeadlineService
from src.user.dependens.auth_guard import authenticate
from src.user.user_schema import ResponseUser

router = APIRouter()


@router.post('/create_headline', response_model=HeadlineResponse)
async def create_headline(request: HeadlineCreate, service: HeadlineService = Depends(),
                          user: ResponseUser = Depends(authenticate)):
    return await service.create_headline(request=request)


@router.get('/headlines', response_model=List[HeadlineResponse])
async def get_all_headlines(service: HeadlineService = Depends(), user: ResponseUser = Depends(authenticate)):
    return await service.get_all_headlines()


@router.get('/get_headline/{headline_id}/', response_model=HeadlineResponse)
async def get_headline(id: int, service: HeadlineService = Depends(), user: ResponseUser = Depends(authenticate)):
    return await service.get_headline(id=id)


@router.put('/update_headline/{file_id}/', response_model=HeadlineResponse)
async def update_headline(request: dict, file_id: int, service: HeadlineService = Depends(),
                          user: ResponseUser = Depends(authenticate)):
    print(file_id, request)
    return await service.update_headline(id=file_id, request=request)


@router.delete('/delete_headline/{headline_id}/', response_model=HeadlineResponse)
async def delete_headline(headline_id: int, service: HeadlineService = Depends(), user: ResponseUser = Depends(authenticate)):
    return await service.delete_headline(id=headline_id)
