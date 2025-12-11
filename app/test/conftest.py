# 코드 전반이 비동기 방식으로 제작되었기 때문에 비동기 방식 테스트를 채택함
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db
from app.config import settings

# Fixtures : 테스트 환경을 특정 상태로 유지하여 일관적인 테스트 환경을 제공하는 기능
# @Pytest.fixture을 사용하여 반복적인 테스트 데이터를 자동으로 생성 가능

# 테스트용 DB와 실제 DB를 분리
TEST_DATABASE_URL = "임시코드(만들면 넣기)"

# 테스트용 비동기 엔진/세션 생성
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    test_engine, class_ = AsyncSession, expire_on_commit=False
)

# 테스트용 DB 세션 의존성
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

# 앱의 DB 의존성을 테스트용 DB로 교체
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="session")
async def db_setup():
    # 테스트 시작 전에 테이블 생성, 종료 후 삭제(임시기 때문에)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="module")
async def async_client(db_setup):
    # 테스트 전체에서 사용할 비동기 HTTP 클라이언트 제공
    async with AsyncSession(app=app, base_url="http://test") as client:
        yield client

