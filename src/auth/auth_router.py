from fastapi import Depends, APIRouter, HTTPException
from fastapi.openapi.models import Response
from fastapi.security import HTTPAuthorizationCredentials
from jose import ExpiredSignatureError, jwt

from src.auth.auth_schema import RegisterUser, AuthUser, ResponseAuthUser
from src.auth.auth_services import AuthService
from src.user.dependens.auth_guard import authenticate, security
from src.user.user_schema import ResponseUser

router = APIRouter()


@router.post('/registration')
async def registration(request: RegisterUser, service: AuthService = Depends()):
    try:
        return await service.registration(request=request)
    except HTTPException as exec:
        raise exec


@router.post('/authorization', response_model=ResponseAuthUser)
async def authorization(request: AuthUser, service: AuthService = Depends()):
    try:
        return await service.authorization(request=request)
    except HTTPException as exec:
        raise exec


@router.get('/confirm_email')
async def confirm_email(user: str, service: AuthService = Depends()):
    try:
        return await service.confirm_email(user=user)
    except HTTPException as exec:
        raise exec


@router.get('/refresh_tokens')
async def refresh_tokens(service: AuthService = Depends(),
                         credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return await service.refresh_tokens(credentials=credentials)
    except HTTPException as exec:
        raise exec
