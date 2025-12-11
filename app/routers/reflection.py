from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import Session
from app import models, schemas
import random

router = APIRouter()

# 코드 테스트하려고 잠시 주석처리, 나중에 풀어주세용
#@router.get("/random", response_model=schemas.ReflectionQuestionResponse)
#def get_random_question(db: Session = Depends(get_db)):

#    question = db.query(models.ReflectionQuestion).all()
#    if not questions:
#        return {"id": 0, "question": "질문이 아직 준비되지 않았습니다."}
    
#    question = random.choice(questions)
#    return question