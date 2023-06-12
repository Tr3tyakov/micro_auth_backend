from fastapi import UploadFile, Form, File
from pydantic import BaseModel


class ImageBase(BaseModel):
    file: UploadFile = File(...)
    alert_id: int = Form(...)


class ImageResponse(BaseModel):
    id: int
    url: str


class CreateImage(ImageBase):
    pass
