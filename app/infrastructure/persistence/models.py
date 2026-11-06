#数据库模型（表，以及关联）
from sqlalchemy import Boolean, Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

#用户
class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),unique=True,nullable=False,index=True)
    password=Column(String(255),nullable=False)
    created_at=Column(DateTime,default=datetime.now)

    #关联表：一个用户有多条评论，多个文章
    articles=relationship("Article",back_populates="author_info")
    comments=relationship("Comment",back_populates="user_info")

    is_deleted=Column(Boolean,default=False)
#文章
class Article(Base):
    __tablename__="articles"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(100),nullable=False)
    content=Column(Text,nullable=False)
    author_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at=Column(DateTime,default=datetime.now)

    #一个文章有多个评论
    author_info=relationship("User",back_populates="articles")
    comments=relationship("Comment",back_populates="article_info")

    is_deleted=Column(Boolean,default=False)
    view=Column(Integer,default=0)
#评论
class Comment(Base):
    __tablename__="comments"

    id=Column(Integer,primary_key=True,index=True)
    content=Column(Text,nullable=False)
    article_id=Column(ForeignKey('articles.id'),nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at=Column(DateTime,default=datetime.now)

    article_info=relationship("Article",back_populates="comments")
    user_info=relationship("User",back_populates="comments")

    is_deleted=Column(Boolean,default=False)