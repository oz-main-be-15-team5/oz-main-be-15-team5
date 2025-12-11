from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated

# 이걸 추후 일기 등 여러곳에 접근 가능하게...

# JWT 디코딩 함수
from app.security import decode_access_token

# DB 세션 의존성
from app.db import get_db

# User 모델
from app.models import User

# tokenUrl : 토큰을 얻는 엔드포인트(main.py의 /auth/token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    # 1. 헤더에서 토큰 추출 및 유효성 검사
    token: Annotated[str, Depends(oauth2_scheme)],
    # 2. DM 세션 가져오기
    db: AsyncSession = Depends(get_db),
) -> User:
    # 현재 로그인된 사용자 정보를 JWT 토큰에서 추출하여 반환
    # decode_access_token에서 JWTError 발생시 HTTPException(401) 처리
    payload = decode_access_token(token)

    # 2. 토큰에서 사용자 ID추출
    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 정보를 찾을 수 없습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. 사용자 ID로 DB에서 User 객체 조회
    user_id = int(user_id_str)
    result = await db.execute(select(User).where(User.id == user_id))
    current_user = result.scalars().first()

    if current_user is None:
        # DB에 해당 ID의 사용자가 없을 때
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 해당하는 사용자가 존재하지 않습니다.",
            headers={"www-Authenticate": "Bearer"},
        )

    # 4.User 객체 반환
    return current_user
