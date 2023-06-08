from fastapi import FastAPI
from src.auth.auth_router import router as auth_router

app = FastAPI()

# app.mount('/micro_alerts/static', StaticFiles(directory='src/static/uploaded_files'))

app.include_router(router=auth_router, prefix='/auth', tags=['auth'])

