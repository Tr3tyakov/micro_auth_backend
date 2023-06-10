from fastapi import Depends, APIRouter, HTTPException, Header

from src.auth.auth_services import AuthGuardService
from src.user.dependens.auth_guard import authenticate
from src.user.user_schema import ResetPassword, ResponseUser
from src.user.user_service import UserService

router = APIRouter()


@router.get('/get_all_users')
async def get_all_users(service: UserService = Depends(), user: ResponseUser = Depends(authenticate)):
    return await service.get_all_user()


@router.get('/get_info')
async def get_info(user: ResponseUser = Depends(authenticate)):
    return user


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
