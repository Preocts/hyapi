"""Player Guild Object"""
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import NamedTuple


class PlayerGuild(NamedTuple):
    """Player Guild Object"""

    id: str = ""
    player: str = ""
    name: str = ""
    raw_data: Dict[str, Any] = {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlayerGuild:
        """Create Player Guild object from dictionary"""
        return cls(
            id=data.get("id", ""),
            player=data.get("player", ""),
            name=data.get("name", ""),
            raw_data=data,
        )
