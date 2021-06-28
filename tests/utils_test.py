"""Unit tests for utils.py"""
import pytest
from hyapi.utils import is_valid_java_name
from hyapi.utils import is_valid_uuid


@pytest.mark.parametrize(
    ("uuid", "expected"),
    (
        ("f498513c-e8c8-4773-be26-ecfc7ed5185d", True),
        ("f498513c-e8c8-4773-be26-ecfc7ed5185d", True),
        ("f498513c-e8c8-4773-be26-ecfc7ed5185d ", False),
        ("", False),
    ),
)
def test_is_valid_uuid(uuid: str, expected: bool) -> None:
    """Validate uuid forms"""
    assert is_valid_uuid(uuid) == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    (
        ("Preocts", True),
        ("Thisisareallylongnamethatwontwork", False),
        ("This?NameFails", False),
        ("This_is_valid", True),
        ("123", True),
        ("This is bad", False),
    ),
)
def test_validate_user_names(name: str, expected: bool) -> None:

    assert is_valid_java_name(name) == expected
