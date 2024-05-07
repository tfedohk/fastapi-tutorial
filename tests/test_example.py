import pytest

# # 일반 테스트 코드를 작성하는 경우
# @pytest.mark.parametrize("test_list,expected", [([3, 5], 8),
#                                                 ([1, 2], 3)] )
# def test_sum(test_list, expected):
#     assert sum(test_list) != expected


# 비동기 테스트 코드를 작성하는 경우
@pytest.mark.asyncio
@pytest.mark.parametrize("test_list,expected", [([3, 5], 8), ([1, 2], 3)])
async def test_sum(test_list, expected):
    assert sum(test_list) == expected
