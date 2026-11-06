from fastapi import HTTPException, Request

from app.api_deps.types import RedisClient

#基于redis的接口限流（固定窗口计数器）
#限流依赖

def rate_limit(max_requests: int,window_seconds: int):
    """限流工厂：每分钟最多请求max_requests 次"""
    def dependency(
            request: Request,
            r:RedisClient
            ):
        #以客户端IP 和请求路径作为限流key
        client_ip=request.client.host
        path= request.url.path
        key= f"rate_limit:{client_ip}:{path}"

        #获取当前请求次数
        current=r.get(key)
        if current and int(current) >= max_requests:
            raise HTTPException(status_code=429,detail="请求过于频繁，请稍后再试！")

        #自增并设置过期时间（第一次请求时设置）
        r.incr(key)
        if not current:
            r.expire(key,window_seconds)
    return dependency
