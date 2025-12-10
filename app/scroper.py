import asyncio
import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession
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
                    "content" : quote_content
                    "author" : quote_author
                })

            return quote_data
        
        except httpx.HTTPStatusError as e:
            print(f"HTTP ERROR: {e}")
            return []
        except Exception as e:
            print(f"Scraping Error: {e}")
            return []
        

