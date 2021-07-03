"""Player Status Object"""
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import NamedTuple


class Session(NamedTuple):
    """Game Object"""

    online: bool = False
    gametype: str = ""
    mode: str = ""
    map: str = ""

    @classmethod
    def from_session(cls, session: Dict[str, Any]) -> Session:
        """Create from inner record"""
        return cls(
            online=session.get("online", False),
            gametype=session.get("gameType", ""),
            mode=session.get("mode", ""),
            map=session.get("map", ""),
        )


class PlayerStatus(NamedTuple):
    """Player Status Object"""

    success: bool = False
    uuid: str = ""
    session: Session = Session()
    raw_data: Dict[str, Any] = {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlayerStatus:
        """Create Player Status object from dictionary"""
        return cls(
            success=data.get("success", False),
            uuid=data.get("uuid", ""),
            session=Session.from_session(data.get("session", {})),
            raw_data=data,
        )
