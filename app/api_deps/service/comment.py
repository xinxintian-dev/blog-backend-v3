from app.api_deps.types import CommentReadrepo, CommentWriterepo, RedisClient
from app.application.services.comment_service import CommentService


#---comment---
def get_comment_write_service(
        repo: CommentWriterepo,
        r:  RedisClient
)->CommentService:
    return CommentService(repo,cache=r)

def get_comment_read_service(
        repo:CommentReadrepo,
        r:  RedisClient
)->CommentService:
    return CommentService(repo,cache=r)

