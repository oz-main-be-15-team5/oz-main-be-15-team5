from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # CORS 미들웨어 임포트
from dotenv import load_dotenv
from app.routers import auth, diary

from app.db import Base, engine


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
# CORS(Cross-Origin Resource Sharing) 설정 추가
# 보안상의 이유로, 웹 브라우저는 다른 도메인, 포트, 프로토콜을 가진 서버(출처, Origin)로 요청을 보낼 때 기본적으로 이를 제한합니다. 이를 **동일 출처 정책(Same-Origin Policy)**이라고 합니다.
# 예를 들어, 프론트엔드 웹사이트가 http://localhost:3000에서 실행되고 있고, 백엔드 API 서버가 http://localhost:8000에서 실행된다면, 브라우저는 이 요청을 교차 출처(Cross-Origin) 요청으로 간주하고 보안상의 이유로 차단합니다.
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500", 
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"], # 모든 HTTP 메서드를 허용한다.
    allow_headers=["*"], # 모든 헤더를 허용한다.
)
# -----------------------

# 라우터 포함
app.include_router(auth.router, prefix="/auth", tags=["인증"])
app.include_router(diary.router, prefix="/diaries", tags=["Diaries"])


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

