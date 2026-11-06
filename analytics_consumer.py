
import json
from kafka import KafkaConsumer
from collections import defaultdict

# 模拟用于统计的内存字典（真实环境这里应该写入 ClickHouse 或 Redis）
article_view_count = defaultdict(int)

print("启动消费者，正在监听 user_behavior 主题...")

def safe_json_deserializer(m):
    try:
        if m is None:
            return {}
        return json.loads(m.decode('utf-8'))
    except json.JSONDecodeError:
        # 遇到无法解析的脏数据，返回空字典直接跳过
        print(f"⚠️ 发现无法解析的脏数据，已跳过: {m}")
        return {}
    
# 连接 Kafka，指定主题，并设置自动提交 offset
consumer = KafkaConsumer(
    'user_behavior',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=safe_json_deserializer,
    auto_offset_reset='earliest',
    group_id='analytics_test_group' # 消费者组
)

for message in consumer:
    log = message.value
    if not log:
        continue
    if log.get("event_type") == "view":
        article_id = log["article_id"]
        article_view_count[article_id] += 1
        
        # 这里是模拟：每来一条日志，就更新一下总览
        print(f"收到浏览日志！文章 ID: {article_id}, 当前累计浏览量: {article_view_count[article_id]}")
        
        # 【进阶】真实场景下，这里会每隔 5 秒把聚合数据批量写入 Redis：
        # redis.hset("article_ranking", str(article_id), article_view_count[article_id])