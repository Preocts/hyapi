"""
Player object from Hypixel public API

Author: Preocts <Preocts#8196>
"""
import json
import logging
from typing import Any
from typing import Dict

import urllib3
from hyapi.authuser import AuthUser
from hyapi.models.playerdata import PlayerData


class Player(AuthUser):
    """Player object"""

    API = "https://api.hypixel.net/player"
    logger = logging.getLogger("Player")

    def __init__(self) -> None:
        """Creates an instance of the player class"""
        super().__init__()

        self.http_client = urllib3.PoolManager(retries=urllib3.Retry(total=2))
        self.headers = {"Accept": "application/json"}

        self._loaded = PlayerData()

    @property
    def read(self) -> PlayerData:
        """Returns loaded PlayerData"""
        return self._loaded

    def load_data(self, id: str) -> None:
        """Loads a player data by account name or UUID"""
        if not self.is_valid_user(id):

            self._loaded = PlayerData()

        else:

            fields = {"uuid": self.user_uuid, "key": self.user_apikey}

            result = self.http_client.request("GET", self.API, fields, self.headers)

            self._loaded = PlayerData.from_dict(self.jsonify(result.data))

            if self._loaded.raw_data:
                self.logger.info("Player '%s' loaded", self._loaded.uuid)
            else:
                self.logger.warning("Could not load player: '%s'", id)

    def load_friends(self, id: str) -> None:
        """Loads a player's friends list by account name or UUID"""

    def jsonify(self, data: bytes) -> Dict[str, Any]:
        """Translate response bytes to dict, returns empty if fails"""
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return {}
