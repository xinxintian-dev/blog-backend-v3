from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.article.repository import ArticleRepository
from app.domain.comment.repository import CommentRepository
from app.domain.user.repository import UserRepository
from app.infrastructure.persistence.article_repo import SQLAlchemyArticleRepository
from app.infrastructure.persistence.database import get_master_db, get_slave_db
from app.infrastructure.persistence.user_repo import SQLAlchemyUserRepository
from app.infrastructure.persistence.comment_repo import SQLAlchemyCommentRepository

def get_article_db_write_repo(db: Session = Depends(get_master_db))-> ArticleRepository:
    repo=SQLAlchemyArticleRepository(db)
    return repo

def get_article_db_read_repo(db: Session = Depends(get_slave_db))-> ArticleRepository:
    repo=SQLAlchemyArticleRepository(db)
    return repo

def get_user_db_write_repo(db: Session = Depends(get_master_db))-> UserRepository:
    repo=SQLAlchemyUserRepository(db)
    return repo

def get_user_db_read_repo(db: Session = Depends(get_slave_db))-> UserRepository:
    repo=SQLAlchemyUserRepository(db)
    return repo

def get_comment_db_write_repo(db: Session = Depends(get_master_db))-> CommentRepository:
    repo=SQLAlchemyCommentRepository(db)
    return repo

def get_comment_db_read_repo(db: Session = Depends(get_slave_db))-> CommentRepository:
    repo=SQLAlchemyCommentRepository(db)
    return repo