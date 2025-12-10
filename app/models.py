from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import datetime
from datetime import datetime
from app.db import Base

class Diary(Base):
    __tablename__ = "diaries"
    
    id = Cloumn(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="diaries")
    