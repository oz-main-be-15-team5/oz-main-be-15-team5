# 입력/출력 데이터를 정의
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# 1. 데이터베이스 모델과 직접적으로 연결되지 않는 기본 설정을 위한 클래스
# class BaseSchema(BaseModel):
# 유연한 모델 생성을 위해 허용되지 않는 필드를 무시하도록 설정
# Schema 형식 통일을 위해 주석처리
#    class Config:
#        from_attributes = True


# --------------------------
# 1. 유저 조회 스키마
# --------------------------
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# --------------------------
# 1. 유저 조회 스키마
# --------------------------
class UserBase(BaseModel):
    # 클라이언트에게 노출되는 사용자 기본 정보
    # 비밀번호 등의 민감 정보가 포함되어서는 안됨
    # user_id: int >> models.User의 id와 일치하도록 필드명을 수정
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        # --------------------------

class UserWithBookmark(UserBase):
    quote_id: int | None = None

# --------------------------
# 2. 회원가입 스키마
# --------------------------
# 상속을 통한 모델 확장
class UserCreate(BaseModel):
    # 회원가입을 위한 데이터 검증
    username: str = Field(..., max_length=100)
    email: EmailStr = Field(..., max_length=100)
    # 유저 비밀번호(출력/응답용)
    # UserBase 상속으로 개인정보 보안을 위해 비밀번호 별도 분리
    # 최소 글자수 제한을 두어 보안성 증가
    password: str = Field(..., min_length=6)
    # 비밀번호 확인 필드
    password_confirm: str = Field(..., min_length=6)
    # 시간나면 추가 : 비밀번호와 비밀번호 확인이 일치하는지 확인하는 모델 유효성 검사
# --------------------------

# --------------------------
# 3. 로그인 및 토큰 스키마
# --------------------------
class UserLogin(BaseModel):
    # 로그인 요청시 입력 데이터
    # 회원가입시 아이디/이메일 작성 요구하기 때문에
    username_or_email: str = Field(...)
    password: str = Field(...)

class Token(BaseModel):
    # JSON 토큰 정보
    access_token: str
    # bearer : 토큰 기본 타입
    token_type: str = "bearer"
# --------------------------

# --------------------------
# 4. 명언 스키마
# --------------------------
class QuoteBase(BaseModel):
    id: int
    content: str
    author: str | None = None

    class Config:
        from_attributes = True

# 북마크 상태 표시
class QuoteResponse(QuoteBase):
    is_bookmarked: bool = False
# --------------------------


class DiaryBase(BaseModel):
    title: str
    content: str


class DiaryCreate(DiaryBase):
    pass


class DiaryUpdate(DiaryBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # orm_mode = True 대신 사용
        from_attributes = True


class ReflectionQuestionResponse(BaseModel):
    id: int
    question: str
    
    class Config:
        orm_mode = True