// quote.html의 <script> 태그 내부 (기존 함수들 사이에 추가)

// 로그아웃 함수: 토큰 삭제 후 로그인 페이지로 리디렉션
function logoutAndRedirect() {
    if (confirm("정말 로그아웃 하시겠습니까?")) {
        localStorage.removeItem('accessToken');
        // 토큰을 삭제하고 로그인 페이지로 이동
        window.location.href = 'index.html'; 
    }
}

// ----------------------------------------------------
// 기존 코드: 페이지 로드 시 로그인 상태 체크 부분을 수정
// ----------------------------------------------------
if (!accessToken) {
    alert("로그인이 필요합니다. 로그인 화면으로 돌아갑니다.");
    window.location.href = 'index.html'; // 로그인 페이지로 리디렉션
}