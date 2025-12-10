from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


# User 모델 정의
class User(Base):

    #없애면 오류남...
    __tablename__ = "users"

    # user ID
    id = Column(Integer, primary_key=True, index=True)

    # 비밀번호 해시 : 암호화된 비밀번호 저장
    # 보안을 위해 평문 비밀번호는 X
    password_hash = Column(String(255), nullable=False)

    # 유저명 (UNIQUE)
    username = Column(String(100), unique=True, nullable=False)

    # 이메일 (UNIQUE)
    email = Column(String(100), unique=True, nullable=False)

    # 가입일시 (자동생성)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Diary와의 역방향 관계
    diaries = relationship("Diary", back_populates="user")

    # 파이썬 객체를 문자열로 반환하도록 정의
    def __str__(self):
        return self.username


class Diary(Base):
    __tablename__ = "diaries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="diaries")
    