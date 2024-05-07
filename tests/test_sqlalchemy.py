# import pytest

# from sqlalchemy import text
# from sqlalchemy.ext.asyncio import AsyncSession


# @pytest.mark.asyncio  # 비동기 함수 돌릴 때 쓰는 데코레이터
# async def test_db_connection(async_session: AsyncSession):
#     result = (
#         await async_session.execute(text("SELECT 1"))
#     ).scalar()  # DB에 ping 찍어보는 것

#     assert result == 1
