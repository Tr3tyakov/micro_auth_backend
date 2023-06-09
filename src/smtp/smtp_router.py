from fastapi import Depends, APIRouter, HTTPException

from src.smtp.smtp_schema import CreateSMTP
from src.smtp.smtp_service import SMTPService
from src.user.user_service import UserService

router = APIRouter()


@router.get('/get_information')
async def get_smtp_information(service: SMTPService = Depends()):
    try:
        return await service.get_information()
    except HTTPException as exec:
        raise exec


@router.post('/set_information')
async def set_smtp_information(request: CreateSMTP, service: SMTPService = Depends()):
    try:
        return await service.set_information(request=request)
    except HTTPException as exec:
        raise exec


@router.post('/send_message')
async def send_message(service: SMTPService = Depends()):
    try:
        return await service.send_message()
    except HTTPException as exec:
        raise exec
