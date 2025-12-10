from aqlalchemy import create_engine
from sqlalchemy.ext.declaractive import declaractive_base
from sqlalcehmy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/mydiary"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declaractive_base()

def get_db():
    db = SessionLocal()
    try:
      yield db
    finally:
        db.close()