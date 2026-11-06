from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from app.config import settings
#主库（负责写）：真实场景换成你的Master IP
MASTER_URL=settings.DB_MASTER_URL
#从库（负责读）:真实场景换成你的Slave IP
SLAVE_URL=settings.DB_SLAVE_URL

master_engine=create_engine(
    MASTER_URL,
    pool_pre_ping=True,
    pool_recycle=3600
    )
slave_engine=create_engine(
    SLAVE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
    )

MasterSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=master_engine)
SlaveSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=slave_engine)

class Base(DeclarativeBase):
    pass

#提供两个依赖
def get_master_db():
    db=MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_slave_db():
    db=SlaveSessionLocal()
    try:
        yield db
    finally:
        db.close()