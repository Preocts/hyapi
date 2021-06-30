"""Unit tests for player.py"""
from typing import Generator

import pytest
from hyapi.player import Player

# TODO: VCR Recording needed


@pytest.fixture(scope="function", name="player")
def fixture_player() -> Generator[Player, None, None]:
    """Build a fixture"""
    player = Player()

    yield player


def test_hold(player: Player) -> None:
    """Holding pattern"""
    assert not player.current_player
