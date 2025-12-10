from fastapi import FastAPI, APIRouter, HTTPException
from tortoise import Tortoise
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# 비밀번호 해싱을 위한 import
from app.users import register_user
from app.schemas import UserCreate, UserBase, UserLogin, Token
from app.auth_service import login_for_access_token
from app.routers import auth, diary
from app.db import Base, engine

load_dotenv()


# -----------------------
# 데이터베이스 연결
# 모델 정의
# -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 앱 시작시 실행
    db_url = os.getenv("DATABASE_URL")

    await Tortoise.init(db_url=db_url, modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()

    yield  # 앱실행

    # 앱 종료시 실행
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)
auth_router = APIRouter(prefix="/auth", tags=["인증"])


# -----------------------
# 회원가입 : 새 사용자 등록
# -----------------------
@auth_router.post("/register", response_model=UserBase)
async def handle_user(user_data: UserCreate):
    try:
        # 비밀번호 해싱 및 DB저장
        new_user_db = await register_user(user_data)
        return new_user_db

    except Exception as e:
        # UNIQUE 예외처리(외 DB제약 조건 위반)
        raise HTTPException(status_code=500, detail=f"사용자 등록 실패: {e}")


app.include_router(auth_router)

# -----------------------


# -----------------------
# 로그인 앤드포인트 추가
# -----------------------
@auth_router.post("/token", response_model=Token)
async def login(user_data: UserLogin):
    # 사용자 인증 후 JWT 토큰 반환
    token = await login_for_access_token(user_data)
    return token


# -----------------------


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Diary Project")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(diary.router, prefix="/diaries", tags=["Diaries"])
