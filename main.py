from fastapi import FastAPI
from src.auth.auth_router import router as auth_router
from src.user.user_router import router as user_router
from src.smtp.smtp_router import router as smtp_router

app = FastAPI()

# app.mount('/micro_alerts/static', StaticFiles(directory='src/static/uploaded_files'))

app.include_router(router=auth_router, prefix='/auth', tags=['auth'])
app.include_router(router=user_router, prefix='/user', tags=['user'])
app.include_router(router=smtp_router, prefix='/smtp', tags=['smtp'])
