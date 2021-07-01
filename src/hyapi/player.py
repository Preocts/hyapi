"""
Player object from Hypixel public API

Author: Preocts <Preocts#8196>
"""
from __future__ import annotations

import json
import logging
from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional

import urllib3
from hyapi.authuser import AuthUser


class Player(AuthUser):
    """Player object"""

    API = "https://api.hypixel.net/player"
    logger = logging.getLogger("Player")

    def __init__(self) -> None:
        """Creates an instance of the player class"""
        super().__init__()

        self.http_client = urllib3.PoolManager(retries=urllib3.Retry(total=2))
        self.headers = {"Accept": "application/json"}

        self._loaded = PlayerObject()

    @property
    def read(self) -> PlayerObject:
        """Returns loaded PlayerObject"""
        return self._loaded

    def load(self, id: str) -> None:
        """Loads a player by account name or UUID"""
        if not self.is_valid_user(id):

            self._loaded = PlayerObject()

        else:

            fields = {"uuid": self.user_uuid, "key": self.user_apikey}

            result = self.http_client.request("GET", self.API, fields, self.headers)

            self._loaded = PlayerObject.from_dict(self.jsonify(result.data))

            if self._loaded.raw_data:
                self.logger.info("Player '%s' loaded", self._loaded.uuid)
            else:
                self.logger.warning("Could not load player: '%s'", id)

    def jsonify(self, data: bytes) -> Dict[str, Any]:
        """Translate response bytes to dict, returns empty if fails"""
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return {}


class PlayerObject(NamedTuple):
    """Player Object"""

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
    def from_dict(cls, in_dict: Dict[str, Any]) -> PlayerObject:
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
