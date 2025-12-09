from fastapi import FastAPI
from tortoise import Tortoise, fields
from tortoise.models import Model
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()


# 모델 정의
class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 앱 시작시 실행
    db_url = os.getenv("DATABASE_URL")

    await Tortoise.init(db_url=db_url, modules={"models": ["app.main"]})
    await Tortoise.generate_schemas()
    print("데이터베이스 연결 완료")

    yield  # 앱실행

    # 앱 종료시 실행
    await Tortoise.close_connections()
    print("데이터베이스 연결 종료")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.post("/users/")
async def create_user(name: str):
    user = await User.create(name=name)
    return {"id": user.id, "name": user.name}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
