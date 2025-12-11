from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.schemas import UserCreate, Token, UserLogin, UserBase
from app.services.users import register_user
from app.services.auth_service import login_for_access_token  # login_for_access_token 임포트
from app.dependencies import get_current_user  # 인증 의존성 함수
from app.models import User, UserQuoteBookmark  # User 모델


router = APIRouter(prefix="/auth", tags=["인증"])


# -----------------------
# 회원가입 : 새 사용자 등록
# -----------------------
@router.post("/register", response_model=UserCreate)
async def handle_user_register(
    user_data: UserCreate, db: AsyncSession = Depends(get_db)
):
    if user_data.password != user_data.password_confirm:
        # 비밀번호 불일치 시 400 에러
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 2. status 사용
            detail="비밀번호와 비밀번호 확인이 일치하지 않습니다.",
        )

    try:
        # 비밀번호 해싱 및 DB저장
        new_user_db = await register_user(db, user_data)
        return new_user_db

    except Exception as e:
        # UNIQUE 예외처리(외 DB제약 조건 위반)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"사용자 등록 실패: {e}",
        )
# -----------------------


# -----------------------
# 로그인 앤드포인트 추가
# -----------------------
@router.post("/token", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # 사용자 인증 후 JWT 토큰 반환
    token = await login_for_access_token(db, user_data)
    return token
# -----------------------


# -----------------------
# 보호된 앤드포인트
# -----------------------
@router.get("/me", response_model=UserBase)  # UserBase 스키마를 응답 모델로 사용
async def read_users_me(current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):

    # 가장 최근 북마크 하나 조회
    stmt = (
        select(UserQuoteBookmark.quote_id)
        .where(UserQuoteBookmark.user_id == current_user.id)
        .order_by(UserQuoteBookmark.created_at.desc())
        .limit(1)
    )

    result = await db.execute(stmt)
    latest_quote_id = result.scalar_one_or_none()

    # 현재 로그인한 사용자 정보 반환
    # 인증 필요
    return UserBase(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        # 조회된 명언 id 사용
        quote_id=latest_quote_id if latest_quote_id is not None else 0,
        created_at=current_user.created_at,
    )
# -----------------------
