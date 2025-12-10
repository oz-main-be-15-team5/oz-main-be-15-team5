from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.security import decode_access_token
from app.models import User

# 토큰 앤드포인트를 지정해 클라이언트에게 토큰을 얻는 방법을 알려줌...
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # 요청 헤더에서 JWT 토큰 추출 / 유효성 검사
    # 인증된 사용자 DB 객체 반환
#    payload = decode_access_token(token)

    # 사용자 ID 추출
#    user_id = payload.get("sub")
