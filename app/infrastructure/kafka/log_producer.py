from fastapi import logger

from app.domain.logging.acticon_logger import ActionLogger
from kafka import KafkaProducer
import json
import time

class KafkaActionLogger(ActionLogger):
    def __init__(self):
        self.producer=KafkaProducer(
            bootstrap_servers=['127.0.0.1:9092'],
            value_serializer=lambda v:json.dumps(v).encode('utf-8'),
            #设置重试和超时，防止Kafka 挂了卡死主线程
            retries=3,
            request_timeout_ms=5000
        )
    def log_view(self,user_id: int,article_id: int) ->None:
        log_data={
            "event_type": "view",
            "user_id": user_id,
            "article_id": article_id,
            "timestamp": int(time.time())

        }
        try:
            #发送到 user_behavior 主题
            self.producer.send('user_behavior',value=log_data)
            #强制刷新，保证发送出去（真实生产环境为了性能不强制立即发送）
            self.producer.flush()
            logger.info(f"发送行为日志成功：{log_data}")
        except Exception as e:
            logger.error(f"发送行为日志失败，忽略：{e}")