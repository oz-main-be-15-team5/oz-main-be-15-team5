from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from app.db import get_db

router = APIRouter()


# AttributeError: module 'app.schemas' has no attribute 'DiaryResponse'
# 동기DB를 비동기 DB로 바꾼거니까 필요시 주석떼고 바꾸시면 됩니다
# @router.post("/", response_model=schemas.DiaryResponse)
@router.post("/", response_model=schemas.DiaryUpdate)
# def create_diary(diary: schemas.DiaryCreate, db: Session = Depends(get_db)):
async def create_diary(diary: schemas.DiaryCreate, db: AsyncSession = Depends(get_db)):
    new_diary = models.Diary(**diary.dict(), user_id=1)
    db.add(new_diary)
    # db.commit()
    await db.commit()
    # db.refresh(new_diary)
    await db.refresh(new_diary)
    return new_diary


# AttributeError: module 'app.schemas' has no attribute 'DiaryResponse'
# @router.get("/", response_model=list[schemas.DiaryResponse])
@router.get("/", response_model=list[schemas.DiaryUpdate])
# def list_diaries(page: int = 1, size: int = 10, keyword: str = "", db:Session = Depends(get_db)):
async def list_diaries(
    page: int = 1, size: int = 10, keyword: str = "", db: AsyncSession = Depends(get_db)
):

    query = db.query(models.Diary)
    if keyword:
        query = query.filter(
            models.Diary.title.contains(keyword)
            | models.Diary.content.contains(keyword)
        )
    diaries = (
        query.order_by(models.Diary.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return diaries
