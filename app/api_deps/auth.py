from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt,JWTError

from app.infrastructure.security.hasher import PasswordHasher
from app.infrastructure.security.jwt import ALGORITHM, JWTProvider
from app.config import settings
from app.api_deps.types import RedisClient



def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_jwt_provider() -> JWTProvider:
    return JWTProvider()

security=HTTPBearer()

def get_current_user_id(
        credentials:Annotated[HTTPAuthorizationCredentials,Depends(security)],
        r: RedisClient
        )->int:

    """保安: 校验Token是否合法，并返回用户ID"""

    token=credentials.credentials

    #鉴权校验中拦截黑名单token
    #1.先查黑名单
    if r.exists(f"jwt_blacklist:{token}"):
        raise HTTPException(status_code=401,detail="Token 已失效，请重新登录")
        
    try:
        payload=jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[ALGORITHM])
        user_id=int(payload.get("sub"))
        return user_id
    except JWTError:
        raise HTTPException(status_code=401,detail="Token 无效或已过期")
