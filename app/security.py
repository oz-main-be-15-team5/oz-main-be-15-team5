import bcrypt
from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import os
from dotenv import load_dotenv


load_dotenv()


# ----------------------------------------
# JWT 설정
# ----------------------------------------
SECRET_KEY = os.getenv("SECRET_KET", "YOUR_SUPER_SECRET_KEY")
# HS : 대칭키 방식 사용, 서명 생성/검증시 하나의 SECRET_KEY 만 사용
# 256 : HMAC 적용시 SHA-256 해시 함수 사용
# JWT 헤더+페이로드+시크릿키를 256비트(32바이트) 고정된 길이로 변환하는 해시 함수
ALGORITHM = "HS256"
# 접근 토큰 만료 시간
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# ----------------------------------------


# ----------------------------------------
# 비밀번호 해싱 및 검증 함수
# ----------------------------------------
# bcrypt 해시 생성시 사용할 솔트의 작업 부하
# 숫자가 높을수록 해싱에 더 많은 시간이 소요, 보안성이 높아지지만 서버 부하가 커짐
# 12 or 14
BCRYPT_ROUNDS = 12


def get_password_hash(password: str) -> str:
    # 문자열 비민번호를 입력받아 해시된 비밀번호에 문자열을 반환

    # 1. 솔트 생성
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)

    # 2. 비밀번호를 인코딩하고 솔트와 함께 해싱
    hashed_password_bytes = bcrypt.hashpw(password.encode("utf-8"), salt)

    # 3. 해시된 바이트를 문자열로 디코딩하여 반환
    return hashed_password_bytes.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 평문 비밀번호와 해시된 비밀번호를 비교하여 일치하는지 확인

    # 1. 입력된 평문 비밀번호를 인코딩
    plain_password_bytes = plain_password.encode("utf-8")

    # 2. 저장된 해시 비밀번호를 인코딩
    hashed_password_bytes = hashed_password.encode("utf-8")

    # 3. bcrypt.checkpw 함수로 비교
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


# ----------------------------------------


# ----------------------------------------
# JWT 토큰 생성 함수
# ----------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # 데이터 기반 JWT 액세스 토큰 생성
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 기본 만료 시간 적용
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # 만료 시각 처리
    to_encode.update({"exp": expire})

    # 토큰 인코딩
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ----------------------------------------


# ----------------------------------------
# JWT 토큰 검증 함수
# ----------------------------------------
def decode_access_token(token: str) -> dict[str, Any]:
    # 액세스 토큰 디코딩 후 payload(전송 데이터)반환
    # 토큰이 유효하지 않으면 HTTP 401 오류 발생
    try:
        # 1. 토큰 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 2. 주제(sub) 추출
        user_id: Optional[str] = payload.get("sub")

        if user_id is None:
            raise JWTError("Invalid token payload")

        return payload

    except JWTError:
        # 서명 불일치나 만료 발생시
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ----------------------------------------
