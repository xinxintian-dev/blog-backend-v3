from fastapi import APIRouter, Depends
from app.api_deps.auth import get_current_user_id
from app.api_deps.identity import get_optional_user_id
from app.api_deps.service.article import get_article_read_service, get_article_write_service
from app.application.services.article_service import ArticleService
from app.api.schemas.article import ArticleCreate, ArticleResponse
from typing import Annotated
from app.api_deps.rate_limit import rate_limit


router = APIRouter(prefix="/articles", tags=["文章"])

@router.post("/", response_model=ArticleResponse)
def create_article(
    data: ArticleCreate,
    #依赖要求必须传Token，并自动解析出user_id
    current_user_id:Annotated[int,Depends(get_current_user_id)],
    service: Annotated[ArticleService,Depends(get_article_write_service)], 
    _=Depends(rate_limit(max_requests=5,window_seconds=60))
):

    # 调用业务逻辑
    article_entity = service.create_article(data.title, data.content, current_user_id)
    # 把领域实体转成 Pydantic 响应
    return ArticleResponse(
        id=article_entity.id, title=article_entity.title, 
        content=article_entity.content, author_id=article_entity.author_id,
        author_name=article_entity.author_name, created_at=article_entity.created_at
    )

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    service: Annotated[ArticleService,Depends(get_article_read_service)],
    user_id: Annotated[int,Depends(get_optional_user_id)]
):
    article_entity = service.get_article(article_id,user_id)
    return ArticleResponse(
                id=article_entity.id, title=article_entity.title, 
                content=article_entity.content, author_id=article_entity.author_id,
                author_name=article_entity.author_name, created_at=article_entity.created_at
            )

@router.post("/{article_id}/view")
def add_view(
    article_id: int,
    service: Annotated[ArticleService,Depends(get_article_write_service)]
    ):
    service.incr_views(article_id)
    return {"msg":"ok"}
