from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    # 회원가입에 필요한 정보(입력용)
    username: str = Field
    email: EmailStr = Field


class UserCreate(UserBase):
    # 유저 비밀번호(출력/응답용)
    # UserBase 상속으로 개인정보 보안을 위해 비밀번호 별도 분리
    # 최소 글자수 제한을 두어 보안성 증가
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="hong@example.com")
    password: str = Field(..., example="abcd1234")


class BookmarkRead(BaseModel):
    id: int
    quote_id: int
    user_id: int

    class Config:
        orm_mode = True
