import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# .env에서 DB 정보 가져오기
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# PostgreSQL 연결 문자열 형식
DATABASE_URL = f"asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tortoise ORM의 최종 설정 딕셔너리
TORTOISE_CONFIG = {
    # 연결 설정
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            # 모델 파일 경로 지정
            # exaple 임시파일로 경로지정
            # aerich.models Aerich 도구가 작동하기 위한 필수 파일
            # default라는 연결을 앱이 사용하도록 명시적으로 지정
            "models": ["exaple.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Seoul",
}
