from fastapi import APIRouter, Depends, HTTPException
from app.api_deps.service.user import get_user_write_service
from app.application.services.user_service import UserService
from app.api.schemas.user import  UserRegister,UserLogin  # Pydantic 模型放 schemas 下
from typing import Annotated

from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.infrastructure.persistence.redis_client import get_redis

router = APIRouter(prefix="/user", tags=["用户"])

@router.post("/register")
def register(
    data: UserRegister,
    service: Annotated[UserService,Depends(get_user_write_service)]
    ):
    user=service.register(data.username,data.password)
    return {"message": "注册成功", "user_id": user.id}

@router.post("/login")
def login(
    data:UserLogin,
    service:Annotated[UserService,Depends(get_user_write_service)]
    ):
    try:
        return service.login(data.username,data.password)
    except ValueError as e:
        return HTTPException(status_code=401,detail=str(e))

#解决退出账号，token仍然有效
security=HTTPBearer()
@router.post("/logout")
def logout(
    credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)],
    r= Depends(get_redis)
):
    token = credentials.credentials

    #把token加入redis 黑名单，过期时间设置为token的剩余有效期（这里简写为1天）
    r.setex(f"jwt_blacklist:{token}",86400,"1")
    return {"message": "退出登录成功"}