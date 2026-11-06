from kafka import KafkaProducer
import json

# 连接 Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 发送一条结构完全正确的测试消息 (注意这里的 key 和你的代码里一致)
test_data = {
    "event_type": "view",
    "article_id": 1
}

producer.send('user_behavior', test_data)
producer.flush()
print("✅ 已经成功发送了一条正确的 JSON 数据！")