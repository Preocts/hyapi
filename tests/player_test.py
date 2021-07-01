"""Unit tests for player.py"""
import os
from typing import Generator
from unittest.mock import patch

import pytest
import vcr
from hyapi.player import Player

TEST_UUID = "Preocts"
RECORDING_MODE = False

recorder = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/fixtures",
    record_mode="new_episodes" if RECORDING_MODE else "once",
    match_on=["uri", "method"],
    filter_query_parameters=["key"],
)


@pytest.fixture(scope="function", name="player")
def fixture_player() -> Generator[Player, None, None]:
    """Build a fixture"""
    with recorder.use_cassette("vcr_player.yaml"):
        with patch.dict(os.environ, {"HYAPI_APIKEY": "mock"}):

            player = Player()

            yield player


def test_load_player(player: Player) -> None:
    """load player"""

    player.load(TEST_UUID)

    assert player.read.displayname == TEST_UUID
    assert player.read.raw_data


def test_load_error(player: Player) -> None:
    """Empty object"""

    with patch.object(player, "jsonify", return_value={}):

        player.load(TEST_UUID)

        assert not player.read.displayname
        assert not player.read.raw_data


def test_jsonify_valid(player: Player) -> None:
    """Good data makes json happy"""

    valid_bytes = '{"Hello": "There"}'.encode()
    result = player.jsonify(valid_bytes)

    assert result["Hello"] == "There"


def test_jsonify_invalid(player: Player) -> None:
    """Bad data make json frown"""

    invalid_bytes = "Hello There".encode()
    result = player.jsonify(invalid_bytes)

    assert isinstance(result, dict)
    assert not result


def test_invalid_id(player: Player) -> None:
    """Return empty object"""
    with patch.object(player, "is_valid_user", return_value=False):
        player.load(TEST_UUID)

    assert not player.read.raw_data
