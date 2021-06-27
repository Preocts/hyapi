"""Unit tests for uuidlookup.py"""
import pytest
from hyapi.uuidlookup import UUIDLookup

TEST_NAME = "jeb"
TEST_UUID = "f498513c-e8c8-4773-be26-ecfc7ed5185d"


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
    uuidlookup = UUIDLookup()

    assert uuidlookup._is_valid_name(name) == expected


def test_lookup_by_name() -> None:
    uuidlookup = UUIDLookup()

    result = uuidlookup.resolve_by_name(TEST_NAME)

    assert result.name == TEST_NAME
    assert result.id == TEST_UUID.replace("-", "")


def test_invalid_name() -> None:
    """Ensure we don't hit API on invalid names"""
    lookup = UUIDLookup()

    with pytest.raises(ValueError):
        lookup.resolve_by_name("This fails")


def test_no_results() -> None:
    """Use an invalid name to capture failure"""
    lookup = UUIDLookup()

    result = lookup.resolve_by_name("a")

    assert result.name is None
    assert result.id is None
