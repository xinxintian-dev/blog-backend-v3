from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError


from app.config import settings
from app.infrastructure.security import jwt
from app.api_deps.types import RedisClient

#日志记录获取user_id分辨用户和游客
# 实例化一个不自动报错的 security（关键点：auto_error=False）

optional_security = HTTPBearer(auto_error=False)

def get_optional_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(optional_security)],
    r: RedisClient
) -> int:
    """
    尝试解析 Token。如果是合法 Token 则返回 user_id，如果无 Token 或 Token 失效则返回 0（游客）
    """
    # 1. 如果没有传 Authorization 头，直接按游客处理
    if not credentials:
        return 0

    token = credentials.credentials

    # 2. 检查黑名单
    if r.exists(f"jwt_blacklist:{token}"):
        return 0  # Token 已拉黑，按游客处理

    # 3. 解析 Token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[jwt.ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except JWTError:
        return 0  # 解析失败（过期或伪造），按游客处理