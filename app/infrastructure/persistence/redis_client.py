import redis
from redis import ConnectionPool
from app.config import settings
#1.读取配置文件（比如project.toml 或 .env）
# REDIS_HOST = "localhost"
# REDIS_PORT = 6379
# REDIS_DB = 0

REDIS_URL=settings.REDIS_URL

#创建全局唯一的连接池（应用启动时加载一次）
# redis_pool=ConnectionPool(
#     host=REDIS_HOST,
#     port=REDIS_PORT,
#     db=REDIS_DB,
#     decode_response=True,
#     max_connections=20
# )

redis_pool=ConnectionPool.from_url(REDIS_URL,decode_responses=True)

#编写依赖注入函数

def get_redis():
    client=redis.Redis(connection_pool=redis_pool)
    try:
        yield client
    finally:
        pass