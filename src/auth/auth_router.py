from fastapi import Depends, APIRouter, HTTPException
from fastapi.openapi.models import Response

from src.auth.auth_schema import RegisterUser, AuthUser, ResponseAuthUser
from src.auth.auth_service import AuthService

router = APIRouter()


@router.post('/registration')
async def registration(request: RegisterUser, service: AuthService = Depends()):
    try:
        return await service.registration(request=request)
    except HTTPException as exec:
        raise exec


@router.post('/authorization')
async def authorization(request: AuthUser, service: AuthService = Depends()):
    return await service.authorization(request=request)
