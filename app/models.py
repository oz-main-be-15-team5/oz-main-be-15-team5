from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


# -------------------------
# User 모델 정의
# -------------------------
class User(Base):

    # 없애면 오류남...
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


# -------------------------


# -------------------------
# 명언 모델 정의
# -------------------------
class Quote(Base):
    __tablename__ = "quotes"

    # quote ID
    id = Column(Integer, primary_key=True, index=True)

    # 명언 내용
    content = Column(Text, nullable=False)

    # 명언 작가(출처)
    author = Column(String(100), nullable=True)

    # 북마크와 역방향 관계
    bookmarks = relationship("UserQuoteBookmark", back_populates="quote")


# -------------------------


# -------------------------
# 북마크 모델 정의
# -------------------------
class UserQuoteBookmark(Base):
    __tablename__ = "user_quote_bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    # FK : 어떤 사용자가 북마크했는가
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # FK: 어떤 명언을 북마크했나
    quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=False)

    # 북마크 지정 시간
    created_at = Column(DateTime, default=datetime.utcnow)

    # User, Quote와의 관계 정의
    user = relationship("User", back_populates="bookmarks")
    quote = relationship("Quote", back_populates="bookmarks")

    # 북마크 중복 방지
    __table_args__ = (
        UniqueConstraint("user_id", "quote_id", name="uq_user_quote_bookmark"),
    )


# -------------------------


class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="diaries")


class ReflectionQuestion(Base):
    __tablename__ = "reflection_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)