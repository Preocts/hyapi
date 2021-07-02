from __future__ import annotations

from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional


class PlayerData(NamedTuple):
    """Player Data Object"""

    uuid: str = ""
    displayname: Optional[str] = None
    rank: Optional[str] = None
    packagerank: Optional[str] = None
    newpackagerank: Optional[str] = None
    monthlypackagerank: Optional[str] = None
    firstlogin: Optional[int] = None
    lastlogin: Optional[int] = None
    lastlogout: Optional[int] = None
    stats: Optional[Dict[str, Any]] = None
    raw_data: Dict[str, Any] = {}

    @classmethod
    def from_dict(cls, in_dict: Dict[str, Any]) -> PlayerData:
        """Create PlayerObject from dictionary"""
        data = in_dict.get("player", {})
        return cls(
            uuid=data.get("uuid", ""),
            displayname=data.get("displayname"),
            rank=data.get("rank"),
            packagerank=data.get("packageRank"),
            newpackagerank=data.get("newPackageRank"),
            monthlypackagerank=data.get("monthlyPackageRank"),
            firstlogin=data.get("firstLogin"),
            lastlogin=data.get("lastLogin"),
            lastlogout=data.get("lastLogout"),
            stats=data.get("stats"),
            raw_data=data,
        )
