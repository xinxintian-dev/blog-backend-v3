#JWT生成实现

from datetime import datetime,timedelta
from jose import jwt
from app.config import settings

ALGORITHM="HS256"

class JWTProvider:
    def create_token(self,user_id:int)->str:
        expire=datetime.now()+timedelta(days=1) #过期时间
        to_encode={"sub":str(user_id),"exp":expire}
        return jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=ALGORITHM)