from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from database import async_session_maker, get_session
from src.auth.auth_router import router as auth_router
from src.user.graphql.schemas.user_schemas import user_schema

from src.user.user_router import router as user_router
from src.smtp.smtp_router import router as smtp_router

app = FastAPI()

# app.mount('/micro_alerts/static', StaticFiles(directory='src/static/uploaded_files'))


app.mount('/graphql',
          GraphQLApp(schema=user_schema, context_value={'session': get_session()}, on_get=make_graphiql_handler()))

app.include_router(router=auth_router, prefix='/auth', tags=['auth'])
app.include_router(router=user_router, prefix='/user', tags=['user'])
app.include_router(router=smtp_router, prefix='/smtp', tags=['smtp'])
