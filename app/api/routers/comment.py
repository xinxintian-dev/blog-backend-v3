from fastapi import APIRouter, Depends, HTTPException
from app.api_deps.service.comment import get_comment_read_service, get_comment_write_service
from app.application.services.comment_service import CommentService
from app.api.schemas.comment import CommentCreate,CommentResponse  # Pydantic 模型放 schemas 下
from typing import Annotated

router = APIRouter(prefix="/comment", tags=["评论"])

@router.post("/",response_model=CommentResponse)
def create_comment(
    data: CommentCreate,
    service: Annotated[CommentService,Depends(get_comment_write_service)]
    ):
    try:
        comment_entity=service.create_comment(content=data.content,article_id=data.article_id,user_id=data.user_id)
        return CommentResponse(
            id=comment_entity.id,
            content=comment_entity.content,
            article_id=comment_entity.article_id,
            user_id=comment_entity.user_id
        )
    except ValueError as e:
        return HTTPException(status_code=400,detail=str(e))

@router.get("/",response_model=list[CommentResponse])
def list_comment(service: Annotated[CommentService,Depends(get_comment_read_service)]):
    comments=service.list_comment()
    CommentResponse(
            id=comments.id,
            content=comments.content,
            article_id=comments.article_id,
            user_id=comments.user_id
        )
    return []