from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException

from src.articles.article.article_schema import ArticleResponse, ArticleCreate
from src.articles.article.article_service import ArticleService
from src.user.dependens.auth_guard import authenticate
from src.user.user_schema import ResponseUser

router = APIRouter()


@router.get('/get_all_articles/', response_model=List[ArticleResponse])
async def get_all_articles(service: ArticleService = Depends(),
                                user: ResponseUser = Depends(authenticate)):
    try:
        return await service.get_all_articles()
    except HTTPException as exec:
        raise exec


@router.get('/get_articles/{headline_id}', response_model=List[ArticleResponse])
async def get_headline_articles(headline_id: int, service: ArticleService = Depends(),
                                user: ResponseUser = Depends(authenticate)):
    try:
        return await service.get_headline_articles(headline_id=headline_id)
    except HTTPException as exec:
        raise exec


@router.post('/create_article/', response_model=ArticleResponse)
async def create_article(request: ArticleCreate, service: ArticleService = Depends(),
                         user: ResponseUser = Depends(authenticate)):
    try:
        return await service.create_article(request=request)
    except HTTPException as exec:
        raise exec


@router.get('/get_article/{article_id}/', response_model=ArticleResponse)
async def get_article(article_id: int, service: ArticleService = Depends(), user: ResponseUser = Depends(authenticate)):
    try:
        return await service.get_article_by_id(article_id=article_id)
    except HTTPException as exec:
        raise exec


@router.put('/update_article/{article_id}/', response_model=ArticleResponse)
async def update_article(request: dict, article_id: int, service: ArticleService = Depends(),
                         user: ResponseUser = Depends(authenticate)):
    try:
        return await service.update_article(request=request, article_id=article_id)
    except HTTPException as exec:
        raise exec


@router.delete('/delete_article/{article_id}/', response_model=ArticleResponse)
async def delete_article(article_id: int, service: ArticleService = Depends(),
                         user: ResponseUser = Depends(authenticate)):
    try:
        return await service.delete_article(article_id=article_id)
    except HTTPException as exec:
        raise exec
