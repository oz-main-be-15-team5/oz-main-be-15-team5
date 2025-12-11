import pytest
from httpx import AsyncClient
from app.test.conftest import async_client  # conftest.py에서 정의한 픽스처 임포트

# 모든 비동기 테스트 함수에 @pytest.mark.asyncio를 붙여야 한다.
# AAA : Arrange, Act, Assert 순의 테스트 코드 검증 패턴
@pytest.mark.asyncio 
async def test_create_user(async_client: AsyncClient):
    # Arrange(준비)
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    }

    # Act (실행)
    response = await async_client.post("/auth/register", json=user_data)
    
    # Assert (검증)
    assert response.status_code == 201 # 성공적인 생성 상태
    data = response.json()
    assert "id" in data
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

    # 비밀번호는 반환되지 않아야 함 (보안)
    assert "password" not in data

    # 테스트 실행 코드
    # 해당 디렉토리가 있는 폴더로 이동
    # pytest tests/auth_test.py