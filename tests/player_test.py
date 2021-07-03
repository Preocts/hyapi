"""Unit tests for player.py"""
import os
from typing import Generator
from unittest.mock import patch

import pytest
import vcr
from hyapi.player import Player

# TEST_UUID = "0a89731cc40b4c93801f96aa35bdf018"
TEST_UUID = "20455fb4737049589d3cba89d181e413"
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


def test_load_player_success(player: Player) -> None:
    """load player data"""

    player.fetch_player(TEST_UUID)

    assert player.data.uuid == TEST_UUID
    assert player.data.raw_data
    assert player.friends.raw_data
    assert player.games.raw_data
    assert player.status.raw_data


def test_load_player_data_error(player: Player) -> None:
    """Empty object"""

    with patch.object(player, "_jsonify", return_value={}):

        player.fetch_player(TEST_UUID)

        assert not player.data.displayname
        assert not player.data.raw_data
        assert not player.friends.raw_data
        assert not player.games.raw_data
        assert not player.status.raw_data


def test_jsonify_valid(player: Player) -> None:
    """Good data makes json happy"""

    valid_bytes = '{"Hello": "There"}'.encode()
    result = player._jsonify(valid_bytes)

    assert result["Hello"] == "There"


def test_jsonify_invalid(player: Player) -> None:
    """Bad data make json frown"""

    invalid_bytes = "Hello There".encode()
    result = player._jsonify(invalid_bytes)

    assert isinstance(result, dict)
    assert not result


def test_data_invalid_id(player: Player) -> None:
    """Return empty object"""
    with patch.object(player, "is_valid_user", return_value=False):
        player.fetch_player(TEST_UUID)

    assert not player.data.raw_data
    assert not player.friends.raw_data
    assert not player.games.raw_data
    assert not player.status.raw_data
