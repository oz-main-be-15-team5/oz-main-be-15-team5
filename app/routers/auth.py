from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_db
from app.services.auth_service import create_access_token
from app.services.users import register_user
from app.dependencies import get_current_user
from app.models import User, UserQuoteBookmark
from app.schemas import UserCreate, UserLogin, Token, UserBase, UserResponse, UserWithBookmark

router = APIRouter(prefix="/auth", tags=["인증"])


# --------------------------
# 회원가입
# --------------------------
@router.post("/register", response_model=UserResponse)
async def handle_user_register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # 비밀번호 확인
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호와 비밀번호 확인이 일치하지 않습니다."
        )

    try:
        # DB에 사용자 저장 (서비스 레이어)
        new_user = await register_user(db, user_data)
        return new_user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"사용자 등록 실패: {e}"
        )


# --------------------------
# 로그인
# --------------------------
@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="이메일 혹은 비밀번호가 잘못되었습니다.")

    # 비밀번호 확인
    if not user.verify_password(data.password):
        raise HTTPException(status_code=400, detail="이메일 혹은 비밀번호가 잘못되었습니다.")

    # JWT 발급
    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


# --------------------------
# 특정 유저 정보 조회
# --------------------------
@router.get("/me", response_model=UserWithBookmark)
async def get_my_info(current_user: User = Depends(get_current_user)):
    return current_user


# --------------------------
# 특정 유저 + 북마크 포함 조회 (예: /auth/users/5)
# --------------------------
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

    return user
