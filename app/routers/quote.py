from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db import get_db
from app import models, schemas
from app.dependencies import get_current_user
import random # 파이썬 자체에서 랜덤처리를 하기 위해서 호출


router = APIRouter(prefix="/quotes", tags=["명언"])


# --------------------------
# 랜덤 명언 제공
# --------------------------
@router.get("/random", response_model=schemas.QuoteResponse)
async def get_random_quote(
    db: AsyncSession = Depends(get_db),
    # 인증된 사용자의 북마크 여부를 확인하기 위해 인증
    current_user: models.User = Depends(get_current_user)
):
    # 1. 전체 갯수 세기
    count_result = await db.execute(select(func.count(models.Quote.id)))
    total_quotes = count_result.scalar_one_or_none()

    if total_quotes is None or total_quotes == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="명언이 없습니다."
        )
    
    # 2. 랜덤 뽑기
    random_offset = random.randint(0, total_quotes - 1)

    # 3. 랜덤 조회
    # OFFSET은 인덱스 0부터 시작함
    stmt = select(models.Quote).offset(random_offset).limit(1)
    quote_result = await db.execute(stmt)
    quote = quote_result.scalars().first()

    # 4. 북마크 여부 확인
    bookmark_stmt = select(models.UserQuoteBookmark).where(
        models.UserQuoteBookmark.user_id == current_user.id,
        models.UserQuoteBookmark.quote_id == quote.id
    )

    bookmark_exists = await db.execute(bookmark_stmt)
    is_bookmarked = bookmark_exists.scalar_one_or_none() is not None

    # 5. 응답 모델 반환
    return schemas.QuoteResponse(
        id=quote.id,
        content=quote.content,
        author=quote.author,
        is_bookmarked=is_bookmarked
    )
# --------------------------


# --------------------------
# 북마크 추가/해제
# --------------------------
@router.post("/{quote_id}/bookmark", status_code=status.HTTP_200_OK)
async def toggle_bookmakr(
    quote_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. 이미 북마크가 되어있는지부터 확인
    bookmark_stmt = select(models.UserQuoteBookmark).where(
        models.UserQuoteBookmark.user_id == current_user.id,
        models.UserQuoteBookmark.quote_id == quote_id
    )
    bookmark = await db.execute(bookmark_stmt)
    existing_bookmark = bookmark.scalar_one_or_none()

    if existing_bookmark:
        # 3. 이미 존재하면 없애기
        await db.delete(existing_bookmark)
        await db.commit()
        return {"message": "북마크가 해제되었습니다.", "bookmared": False}
    else:
        #  존재하지 않으면 추가
        # UniqueContraint : 중복 방지
        new_bookmark = models.UserQuoteBookmark(
            user_id=current_user.id,
            quote_id=quote_id
        )
        db.add(new_bookmark)

        try:
            await db.commit()
            return {"message": "북마크가 추가되었습니다.", "bookmarked": True}
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="북마크 추가중 오류가 발생했습니다."
            )
        


# --------------------------
# 북마크 조회
# --------------------------
@router.get("/bookmakrs", response_model=list[schemas.QuoteBase])
async def list_bookmarks(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 현재 사용자가 북마크한 관계 조회
    # 관계에 연결된 명언객체를 join을 통해 가져오기
    stmt = (
        select(models.Quote)
        .join(models.UserQuoteBookmark)
        .where(models.UserQuoteBookmark.user_id == current_user.id)
        .order_by(models.UserQuoteBookmark.created_at.desc()) #최신순 정렬
    )

    result = await db.execute(stmt)
    bookmakred_quotes = result.scalars().all()

    return bookmakred_quotes
# --------------------------