"""Player Recent Games Object"""
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple


class Game(NamedTuple):
    """Game Object"""

    date: int
    gametype: str
    mode: str
    map: str
    ended: int

    @classmethod
    def from_game(cls, game: Dict[str, Any]) -> Game:
        """Create from inner record"""
        return cls(
            date=game.get("date", 0),
            gametype=game.get("gameType", ""),
            mode=game.get("mode", ""),
            map=game.get("map", ""),
            ended=game.get("ended", 0),
        )


class PlayerGames(NamedTuple):
    """Player Games Object"""

    success: bool = False
    uuid: str = ""
    games: List[Game] = []
    raw_data: Dict[str, Any] = {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlayerGames:
        """Create PlayerGames object from dictionary"""
        games = [Game.from_game(game) for game in data.get("games", [])]
        return cls(
            success=data.get("success", False),
            uuid=data.get("uuid", ""),
            games=games,
            raw_data=data,
        )
