from sqlalchemy.orm import Session
from app import models, schemas

def create_diary(db: Session, diary: schemas.DiaryCreate, user_id: int):
    new_diary = models.Diary(**diary.dict(), user_id=user_id)
    db.add(new_diary)
    db.commit()
    db.refresh(new_diary)
    return new_diary
