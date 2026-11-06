from typing import Annotated

from fastapi import Depends
import redis

from app.api_deps.db import get_article_db_read_repo
from app.application.services.article_service import ArticleService
from app.domain.article.repository import ArticleRepository
from app.domain.logging.acticon_logger import ActionLogger
from app.infrastructure.kafka.log_producer import KafkaActionLogger
from app.infrastructure.persistence.redis_client import get_redis

#用户行为记录
#行为日志接口装配注入
def get_action_logger() ->ActionLogger:
    return KafkaActionLogger()

def get_action_read_service(
        repo: Annotated[ArticleRepository,Depends(get_article_db_read_repo)],
        action_logger:Annotated[ActionLogger,Depends(get_action_logger)], #注入日志器
        r: Annotated[redis.Redis,Depends(get_redis)]
    )->ArticleService:
    return ArticleService(repo=repo,cache=r,action_logger=action_logger)
