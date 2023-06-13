from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from database import get_session

from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler

from src.articles.headline.graphql.schemas.schemas import headline_schema
from src.auth.auth_router import router as auth_router
from src.articles.headline.headline_router import router as headline_router
from src.articles.article.article_router import router as article_router
from src.user.graphql.schemas.user_schemas import user_schema

from src.user.user_router import router as user_router
from src.smtp.smtp_router import router as smtp_router
from src.images.image_router import router as images_router

app = FastAPI()

# """Имеется проблема с прокидываением Bearer token'a в header'e"""
# app.mount('/graphql_iql',
#           GraphQLApp(schema=user_schema, on_get=make_graphiql_handler()))


app.mount('/graphql_user',
          GraphQLApp(schema=user_schema, on_get=make_playground_handler()))
app.mount('/graphql_headline',
          GraphQLApp(schema=headline_schema, on_get=make_playground_handler()))

app.mount('/micro_auth/static', StaticFiles(directory='src/static/uploaded_files'))

app.include_router(router=auth_router, prefix='/auth', tags=['auth'])
app.include_router(router=user_router, prefix='/user', tags=['user'])
app.include_router(router=smtp_router, prefix='/smtp', tags=['smtp'])
app.include_router(router=images_router, prefix='/images', tags=['images'])

app.include_router(router=headline_router, prefix='/headline', tags=['headline'])
app.include_router(router=article_router, prefix='/article', tags=['article'])
