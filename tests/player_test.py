"""Unit tests for player.py"""
import os
from typing import Generator
from unittest.mock import patch

import pytest
import vcr
from hyapi.player import Player

ENV_FILE = ".env"
ENV_RENAME = ".env_hold_for_tests"

TEST_ENV = {
    "HYAPI_USERUUID": "Preocts",
}

recorder = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/fixtures",
    record_mode="once",
    match_on=["uri", "method"],
)


@pytest.fixture(scope="function", name="player")
def fixture_player() -> Generator[Player, None, None]:
    """Build a fixture"""
    try:
        if os.path.isfile(ENV_FILE):
            os.rename(ENV_FILE, ENV_RENAME)
        with recorder.use_cassette("vcr_layer_test.yaml"):

            with patch.dict(os.environ, TEST_ENV):

                player = Player()

                yield player
    finally:
        if os.path.isfile(ENV_RENAME):
            os.rename(ENV_RENAME, ENV_FILE)


def test_hold(player: Player) -> None:
    """Holding pattern"""
    assert not player.current_player
