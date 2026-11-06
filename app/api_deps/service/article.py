from app.api_deps.types import Notifier, RedisClient, ArticleWriterepo, ArticleReadrepo
from app.application.services.article_service import ArticleService

#---article---
#所有写操作（注册、发文章、写评论）的依赖注入，传MasterSession


def get_article_write_service(
        repo: ArticleWriterepo,
        notifier: Notifier,
        r:  RedisClient
)->ArticleService:
    return ArticleService(repo,cache=r,notifier=notifier)

#所有读操作（查文章列表、查详情）的依赖注入，传SlaveSession
def get_article_read_service(
        repo: ArticleReadrepo,
        r:  RedisClient
)->ArticleService:
    return ArticleService(repo,cache=r)


