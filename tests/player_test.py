"""Unit tests for player.py"""
import pytest
from hyapi.player import Player

TEST_NAME = "jeb"
TEST_UUID = "f498513c-e8c8-4773-be26-ecfc7ed5185d"


def test_valid_uuid_no_name() -> None:
    """Give just a uuid, success"""
    _ = Player(uuid=TEST_UUID)


def test_valid_name_no_uuid() -> None:
    """Give just a name, success"""
    _ = Player(mc_name=TEST_NAME)


def test_valid_name_and_uuid() -> None:
    """Give both, success"""
    _ = Player(uuid=TEST_UUID, mc_name=TEST_NAME)


def test_invalid_uuid() -> None:
    """Raise ValueError"""
    with pytest.raises(ValueError):
        _ = Player(uuid="")


def test_invalid_name() -> None:
    """Raise ValueError"""
    with pytest.raises(ValueError):
        _ = Player(mc_name="Invalid Name")


def test_no_args() -> None:
    """Raise ValueError"""
    with pytest.raises(ValueError):
        _ = Player()
