"""Unit tests for uuidlookup.py"""
from hyapi.uuidlookup import UUIDLookup

TEST_NAME = "jeb"
TEST_UUID = "f498513c-e8c8-4773-be26-ecfc7ed5185d"


def test_lookup_by_name() -> None:
    uuidlookup = UUIDLookup()

    result = uuidlookup.resolve_by_name(TEST_NAME)

    assert result.name == TEST_NAME
    assert result.id == TEST_UUID.replace("-", "")


def test_no_results() -> None:
    """Use an invalid name to capture failure"""
    lookup = UUIDLookup()

    result = lookup.resolve_by_name("a")

    assert result.name is None
    assert result.id is None
