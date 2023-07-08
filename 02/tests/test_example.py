import pytest as pytest


@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (2, 3, 5),
    (3, 4, 7),
])
def test_one(a, b, expected, start_stop_rest_service):
    assert a + b == expected


def test_two(start_stop_rest_service):
    print(f"This is test run with start_stop_rest_service fixture: {start_stop_rest_service}")
