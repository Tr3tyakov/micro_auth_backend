from fastapi import Depends, APIRouter, HTTPException, Header
from typing import List

from src.user.dependens.auth_guard import authenticate
from src.user.user_schema import ResponseUser, UpdateUser
from src.user.user_service import UserService

router = APIRouter()


@router.get('/get_all_users', response_model=List[ResponseUser])
async def get_all_users(service: UserService = Depends(), user: ResponseUser = Depends(authenticate)):
    return_value = await service.get_all_user()
    return return_value


@router.get('/get_info', response_model=ResponseUser)
async def get_info(user: ResponseUser = Depends(authenticate)):
    return user


@router.put('/update_info', response_model=ResponseUser)
async def update_info(request: dict, service: UserService = Depends(), user: ResponseUser = Depends(authenticate)):
    try:
        return await service.update_info(request=request, user=user)
    except HTTPException as exec:
        raise exec


@router.delete('/delete_user')
async def delete_user(service: UserService = Depends(), user: ResponseUser = Depends(authenticate)):
    try:
        return await service.delete_user(user)
    except HTTPException as exec:
        raise exec


@router.post('/reset_password')
async def reset_password(request: dict, service: UserService = Depends(),
                         user: ResponseUser = Depends(authenticate)):
    try:
        return await service.reset_password(request=request, user=user)
    except HTTPException as exec:
        raise exec


@router.post('/forgot_password')
async def forgot_password(request: dict, service: UserService = Depends()):
    try:
        return await service.forgot_password(request=request)
    except HTTPException as exec:
        raise exec
