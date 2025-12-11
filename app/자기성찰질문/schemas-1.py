class ReflectionQuestionResponse(BaseModel):
    id: int
    question: str
    
    class Config:
        orm_mode = True