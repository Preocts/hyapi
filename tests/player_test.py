"""Unit tests for player.py"""
from typing import Generator
from unittest.mock import patch

import pytest
import vcr
from hyapi.player import Player

TEST_ENV = {"HYAPI_USERUUID": "Preocts"}
RECORDING_MODE = False

recorder = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/fixtures",
    record_mode="new_episodes" if RECORDING_MODE else "once",
    match_on=["uri", "method"],
)


@pytest.fixture(scope="function", name="player")
def fixture_player() -> Generator[Player, None, None]:
    """Build a fixture"""
    with recorder.use_cassette("vcr_player.yaml"):

        with patch.object(Player, "is_valid_user", return_value=True):

            player = Player()

        player.user_uuid = TEST_ENV["HYAPI_USERUUID"]

        yield player


def test_hold(player: Player) -> None:
    """Holding pattern"""

    assert not player.current_player

    assert player.is_valid_user
