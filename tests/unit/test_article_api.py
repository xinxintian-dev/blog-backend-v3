from contextlib import asynccontextmanager

from fastapi.testclient import TestClient
import pytest
from app.api_deps.auth import get_current_user_id
from main import app
from app.api_deps.service.article import get_article_write_service,get_article_read_service
from app.application.services.article_service import ArticleService
from tests.fakes.fake_article_repo import FakeArticleRepository
from tests.fakes.fake_cache import FakeCache
from tests.fakes.fake_notifier import FakeNotificationService
# 导入真实的 Redis 依赖函数
from app.infrastructure.persistence.redis_client import get_redis


@asynccontextmanager
async def dummy_lifespan(app):
    # 这里什么都不写，或者只写测试需要的全局初始化
    # 不要去调 init_db() 和连真实数据库
    yield
fake_repo = FakeArticleRepository()
fake_cache=FakeCache()
fake_notifier=FakeNotificationService()


@pytest.fixture()
def client():

    def override_get_article_write_service():
        return ArticleService(repo=fake_repo,cache=fake_cache,notifier=fake_notifier)

    def override_get_article_read_service():
        return ArticleService(repo=fake_repo,cache=fake_cache)

    def override_get_current_user_id():
        return 1
    
    # 在 app.dependency_overrides 区域加上这一行：
    app.dependency_overrides[get_redis] = lambda: fake_cache

    # 1. 替换掉应用的 lifespan
    app.router.lifespan_context = dummy_lifespan

    #应用覆盖
    app.dependency_overrides[get_article_write_service] = override_get_article_write_service
    app.dependency_overrides[get_article_read_service] = override_get_article_read_service
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    with TestClient(app) as test_client:
        yield test_client

    #---Teardown(后置清理)---
    app.dependency_overrides.clear()

def test_create_article_api(client):
    response = client.post("/articles/", json={
        "title": "接口测试",
        "content": "通过 HTTP 层测试",
        "author_id": 1
    })
    assert response.status_code == 200
    assert response.json()["title"] == "接口测试"

