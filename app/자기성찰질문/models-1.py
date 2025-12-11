class ReflectionQuestion(Base):
    __tablename__ = "reflection_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)