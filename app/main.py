import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import register_user
from app.schemas import UserCreate, Token, UserLogin
from app.auth_service import login_for_access_token # login_for_access_token 임포트
# 충돌 해결하면 주석처리한걸로 바꿔주세용
# from app.routers import auth, diary
from app.routers import diary
from app.db import Base, engine, get_db

load_dotenv()

# 비동기 DB 스키마 생성
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# -----------------------
# 데이터베이스 연결
# 모델 정의
# -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 앱 시작시 실행
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)

# -----------------------
# 회원가입 : 새 사용자 등록
# -----------------------
@auth_router.post("/register", response_model=UserCreate)
async def handle_user_register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # 비밀번호 해싱 및 DB저장
        new_user_db = await register_user(user_data)
        return new_user_db

    except Exception as e:
        # UNIQUE 예외처리(외 DB제약 조건 위반)
        raise HTTPException(status_code=500, detail=f"사용자 등록 실패: {e}")
# -----------------------


# -----------------------
# 로그인 앤드포인트 추가
# -----------------------
@auth_router.post("/token", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # 사용자 인증 후 JWT 토큰 반환
    token = await login_for_access_token(db, user_data)
    return token
# -----------------------

# 라우터 포함
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# 비동기 환경에서 동기 방식 호출이라 충돌
# Base.metadata.create_all(bind=engine)

# app 객체 재정의로 충돌
# app = FastAPI(title="My Diary Project")

# auth 라우터가 main.py에 구현되어 있어서 충돌
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(diary.router, prefix="/diaries", tags=["Diaries"])
