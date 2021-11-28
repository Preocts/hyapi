from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple


class Friend(NamedTuple):
    """Friend Object"""

    id: str
    uuidsender: str
    uuidreceiver: str
    started: int

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> Friend:
        """Create from inner record"""
        return cls(
            id=record.get("_id", ""),
            uuidsender=record.get("uuidSender", ""),
            uuidreceiver=record.get("uuidReceiver", ""),
            started=record.get("started", 0),
        )


class PlayerFriends(NamedTuple):
    """Player Friends Object"""

    success: bool = False
    uuid: str = ""
    records: List[Friend] = []
    raw_data: Dict[str, Any] = {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlayerFriends:
        """Create PlayerObject from dictionary"""
        records = [Friend.from_record(record) for record in data.get("records", [])]
        return cls(
            success=data.get("success", ""),
            uuid=data.get("uuid", ""),
            records=records,
            raw_data=data,
        )
