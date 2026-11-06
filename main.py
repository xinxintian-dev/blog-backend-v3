
from fastapi import FastAPI
from app.infrastructure.tasks.view_sync_task import start_scheduler
from app.infrastructure.persistence.database import master_engine,Base
from app.api.routers import article, user, comment 
from contextlib import asynccontextmanager
from app.api.exception_handlers import register_exception_handlers


def init_db():
    Base.metadata.create_all(bind=master_engine)

# 然后在应用启动事件（lifespan / startup）里调用 init_db()：
@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    start_scheduler()
    yield
    
app = FastAPI(title="我的博客 API",lifespan=lifespan)

app.include_router(article.router)
app.include_router(user.router)   
app.include_router(comment.router)  

register_exception_handlers(app)

@app.get("/")
def root():
    return {"message":"博客 API 运行中"}

