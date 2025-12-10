# schemas.py 파일에서 정의한 모델 임포트
from .schemas import UserCreate  # 스키마 임포트
from .security import get_password_hash
from app.models import User


# 회원가입
async def register_user(user_data: UserCreate) -> User:
    # 1. 비밀번호 불러오기(DB저장X)
    plain_password = user_data.password

    # 2. 비밀번호 해싱: 안전한 해시값만들기
    hashed_password = get_password_hash(plain_password)

    # 3. Tortoise ORM으로 데이터베이스에 새 레코드 생성/지정
    new_user = await User.create(
        username=user_data.username,
        email=user_data.email,
        # 해시된 비밀번호 값 넣기
        password_hash=hashed_password,
    )

    return new_user
