from tortoise import Tortoise
from dotenv import load_dotenv  # env에 정의된 환경변수를 불러오기 위함
import os  # 환경변수 접근을 위해 불러오기

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")  # 환경변수에서 데이터베이스 주소 가져오기

# 데이터베이스 설정
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
}


# DB 초기화 함수
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()  # 테이블 자동 생성


# DB 종료 함수
async def close_db():
    await Tortoise.close_connections()
