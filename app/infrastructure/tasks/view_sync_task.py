import logging
import redis
from apscheduler.schedulers.background import BackgroundScheduler
from app.infrastructure.persistence.database import MasterSessionLocal
from app.infrastructure.persistence.redis_client import get_redis,redis_pool
from app.infrastructure.persistence.models import Article as ArticleModel

logger=logging.getLogger(__name__)

def sync_view_to_mysql():
    """定时任务： 把Redis 里的浏览量刷入mysql"""
    redis_client = redis.Redis(connection_pool=redis_pool)
    db=MasterSessionLocal()

    try:
        #我们约定redis 里的key 格式为：article：views：{article_id}
        #用scan_iter 模糊匹配所有带有浏览量的 key
        keys = list(redis_client.scan_iter(match="article:view:*"))

        if not keys :
            return
        logger.info(f"开始同步浏览量，共发现{len(keys)} 个待更新任务")

        for key in keys:
            #解析出article_id
            article_id = int(key.split(":")[-1])
            #获取Redis 中的累加值
            views_to_add= int(redis_client.get(key) or 0)

            if views_to_add > 0:
                #更新MySQL 主库（注意：这里要用主库的Session）
                db.query(ArticleModel).filter(ArticleModel.id==article_id).update(
                    {ArticleModel.views : ArticleModel.views + views_to_add}
                )
                #清除 Redis 里的计数，防止重复刷入
                redis.delete(key)
        db.commit()
        logger.info("浏览量同步 MySQL 成功")
    except Exception as e:
        db.rollback()
        logger.error(f"浏览量同步失败： {e}")
    finally:
        db.close()

#初始化调度器
scheduler=BackgroundScheduler()

def start_scheduler():
    """启动调度器"""
    scheduler.add_job(sync_view_to_mysql,'interval',minutes=5)
    scheduler.start()
    logger.info("定时调度器已启动")