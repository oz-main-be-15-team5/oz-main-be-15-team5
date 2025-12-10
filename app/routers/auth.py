from fastapi import APIRouter

router = APIRouter(prefix="", tags=["인증"])

@router.post("/signup")
def signup():
    return {"msg": "회원가입"}

@router.post("/login")
def login():
    return {"msg": "로그인 후 JWT 발급"}
