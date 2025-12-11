from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from app.schemas import UserLogin, Token
from app.security import verify_password, create_access_token
from datetime import timedelta
from typing import Optional


async def authenticate_user(
    db: AsyncSession, username_or_email: str, password: str
) -> Optional[User]:
    # 사용자 이름, 또는 이메일로 사용자 조회/ 비밀번호 검증
    # 사용자 조회
    result = await db.execute(select(User).where(User.username == username_or_email))
    user = result.scalars().first()

    if not user:
        # 사용자 이름으로 찾지 못했으면 이메일로 조회
        result = await db.execute(select(User).where(User.email == username_or_email))
        user = result.scalars().first()

    # 사용자가 존재하지 않음
    if not user:
        return None

    # 비밀번호 검증
    if not verify_password(password, user.password_hash):
        # 비밀번호 불일치
        return None

    return user  # 인증 성공 시 User 객체 반환


async def login_for_access_token(db: AsyncSession, user_data: UserLogin) -> Token:
    # 로그인 요청 처리 후 JWT 토큰 발급
    # 1. 사용자 인증 시도
    user = await authenticate_user(db, user_data.username_or_email, user_data.password)

    if not user:
        # 인증 실패시 에러
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디, 또는 비밀번호가 올바르지 않습니다.",
            # WWW-AUthenticate : 인증방식에 대한 정보를 담고 있음
            headers={"WWW-AUthenticate": "Bearer"},
        )

    # 2. JWT 액세스 토큰 생성
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        # sub : 주제
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    # 3. 토큰 객체 반환
    return Token(access_token=access_token, token_type="bearer")
