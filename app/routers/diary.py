from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import get_db

router = APIRouter()

# AttributeError: module 'app.schemas' has no attribute 'DiaryResponse'
# @router.post("/", response_model=schemas.DiaryResponse)
@router.post("/", response_model=schemas.DiaryUpdate)
def create_diary(diary: schemas.DiaryCreate, db: Session = Depends(get_db)):
    new_diary = models.Diary(**diary.dict(), user_id=1)
    db.add(new_diary)
    db.commit()
    db.refresh(new_diary)
    return new_diary

# AttributeError: module 'app.schemas' has no attribute 'DiaryResponse'
# @router.get("/", response_model=list[schemas.DiaryResponse])
@router.get("/", response_model=list[schemas.DiaryUpdate])
def list_diaries(page: int = 1, size: int = 10, keyword: str = "", db:Session = Depends(get_db)):
    query = db.query(models.Diary)
    if keyword:
        query = query.filter(models.Diary.title.contains(keyword) | models.Diary.content.contains(keyword))
    diaries = query.order_by(models.Diary.created_at.desc()).offset((page-1)*size).limit(size).all()
    return diaries
