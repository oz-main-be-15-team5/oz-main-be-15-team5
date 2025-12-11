import httpx
from bs4 import BeautifulSoup
from app.db import AsyncSessionLocal
from app.models import Quote

# 스크래핑해올 사이트
SCRAPING_URL = "https://saramro.com/quotes"

async def scrape_quotes():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(SCRAPING_URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            quote_data = []

            for item in soup.select('.quote-item'):
                quote_content = item.select_one('.content').text.strip()
                quote_author = item.select_one('.author').text.strip()

                quote_data.append({
                    "content" : quote_content,
                    "author" : quote_author
                })

            return quote_data
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP ERROR: {e}")
            return []
        except Exception as e:
            print(f"Scraping Error: {e}")
            return []
        

async def save_quotes_to_db(quotes_data):
    # 비동기 세션 생성
    async with AsyncSessionLocal() as db:
        #트랜잭션 시작
        async with db.begin():
            for data in quotes_data:
                #명언 중복 방지
                new_quote = Quote(content=data["content"], author=data["author"])
                db.add(new_quote)

                await db.commit()
                print(f"{len(quotes_data)} 개 명언 북마크 완료.")


# 스크래핑은 개별 로직으로 분류하여 별도 프로세스로 실행하는 것이 좋다.
# 1. DB에 대량으로 쓰는 작업은 동기작업인 경우가 많으며 스크래핑 작업이 완료될까지
# FastAPI의 메인 이벤트 루프를 점유하여 블로킹을 일으킬 수 있다.
# → 서버 전체의 성능 저하를 일으킨다.
# 외부 웹사이트를 참조하므로 네트워크 오류, 외부 웹사이트 구조 변경 등으로 실패 확률이 높다.
# 때문에 스래핑 스크립트가 오류발생으로 중단되어도 주 서버에는 영향을 미치지 않아
# 서버의 연속성이 보장된다.
async def run_scraper():
    print("스크래핑 시작")
    quotes = await scrape_quotes()
    if quotes:
        await save_quotes_to_db(quotes)
    print("스크래핑 종료")