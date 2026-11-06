from typing import Annotated
from fastapi import Depends
import redis
from sqlalchemy.orm import Session
from app.api_deps.db import (
    get_article_db_write_repo, get_article_db_read_repo,
    get_comment_db_read_repo, get_comment_db_write_repo,
    get_user_db_read_repo, get_user_db_write_repo
)
from app.domain.article.repository import ArticleRepository
from app.domain.comment.repository import CommentRepository
from app.domain.user.repository import UserRepository
from app.infrastructure.persistence.database import get_master_db,get_slave_db
from app.infrastructure.persistence.redis_client import get_redis
from app.domain.notification.service import NotificationService
from app.infrastructure.notification.celery_notification_impl import CeleryNotificationServiceImpl

#新增通知服务的装配
def get_notification_service()->NotificationService:
    return CeleryNotificationServiceImpl()

# 定义别名
MasterDB = Annotated[Session, Depends(get_master_db)]
SlaveDB = Annotated[Session, Depends(get_slave_db)]
RedisClient = Annotated[redis.Redis, Depends(get_redis)]
Notifier= Annotated[NotificationService,Depends(get_notification_service)]
ArticleWriterepo= Annotated[ArticleRepository, Depends(get_article_db_write_repo)]
ArticleReadrepo= Annotated[ArticleRepository, Depends(get_article_db_read_repo)]
UserWriterepo= Annotated[UserRepository, Depends(get_user_db_write_repo)]
UserReadrepo= Annotated[UserRepository, Depends(get_user_db_read_repo)]
CommentWriterepo= Annotated[CommentRepository, Depends(get_comment_db_write_repo)]
CommentReadrepo= Annotated[CommentRepository, Depends(get_comment_db_read_repo)]
