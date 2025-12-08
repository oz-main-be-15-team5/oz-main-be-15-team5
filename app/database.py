from tortoise import Tortoise

# 데이터베이스 설정
TORTOISE_ORM = {
    "connections": {
        "default": "postgres://user:dev123@localhost:5432/dbname"  # 데이터 베이스 주소
    },
}


# DB 초기화 함수
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()  # 테이블 자동 생성


# DB 종료 함수
async def close_db():
    await Tortoise.close_connections()
