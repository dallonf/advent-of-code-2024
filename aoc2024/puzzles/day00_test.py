from .day00 import uppercase


def test_uppercase():
    assert uppercase(["one", "two", "three"]) == ["ONE", "TWO", "THREE"]
