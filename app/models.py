from tortoise import fields, models


# Tortoise ORM User 모델 정의
class User(models.Model):
    # user ID
    id = fields.IntField(pk=True)

    # 비밀번호 해시 : 암호화된 비밀번호 저장
    # 보안을 위해 평문 비밀번호는 X
    password_hash = fields.CharField(max_length=255, null=False)

    # 유저명 (UNIQUE)
    username = fields.CharField(max_length=100, unique=True, null=False)

    # 이메일 (UNIQUE)
    email = fields.CharField(max_length=100, unique=True, null=False)

    # 가입일시 (자동생성)
    created_at = fields.DatetimeField(auto_now_add=True)

    # 실제 데이터베이스의 연결될 테이블명
    class Meta:
        table = "users"

    # 파이썬 객체를 문자열로 반환하도록 정의
    def __str__(self):
        return self.username
