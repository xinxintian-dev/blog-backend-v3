from typing import Annotated

from fastapi import Depends
from app.api_deps.auth import get_jwt_provider, get_password_hasher
from app.api_deps.types import RedisClient, UserReadrepo, UserWriterepo
from app.application.services.user_service import UserService
from app.infrastructure.security.hasher import PasswordHasher
from app.infrastructure.security.jwt import JWTProvider


#---user---
def get_user_write_service(
        repo:UserWriterepo,
        r:  RedisClient,
        hasher:Annotated[PasswordHasher,Depends(get_password_hasher)],
        token_provider:Annotated[JWTProvider,Depends(get_jwt_provider)]
)->UserService:
    return UserService(repo,cache=r,hasher=hasher,token_provider=token_provider)

def get_user_read_service(
        repo:UserReadrepo,
        r:  RedisClient
)->UserService:
    return UserService(repo,cache=r)
