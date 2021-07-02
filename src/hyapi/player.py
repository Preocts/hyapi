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
from hyapi.models.playerfriends import PlayerFriends


class Player(AuthUser):
    """Player object"""

    DATA_API = "https://api.hypixel.net/player"
    FRIENDS_API = "https://api.hypixel.net/friends"
    logger = logging.getLogger("Player")

    def __init__(self) -> None:
        """Creates an instance of the player class"""
        super().__init__()

        self.http_client = urllib3.PoolManager(retries=urllib3.Retry(total=2))
        self.headers = {"Accept": "application/json"}

        self._loaded_data = PlayerData()
        self._loaded_friends = PlayerFriends()

    @property
    def read_data(self) -> PlayerData:
        """Returns loaded Player Data"""
        return self._loaded_data

    @property
    def read_friends(self) -> PlayerFriends:
        """Returns loaded Player Friends"""
        return self._loaded_friends

    def log_action(self, id: str, uuid: str, obj: str) -> None:
        """Logger"""
        if uuid:
            self.logger.info("%s loaded for: '%s'", obj, uuid)
        else:
            self.logger.warning("Could not load %s for: '%s'", obj, id)

    def load_data(self, id: str) -> None:
        """Loads a player data by account name or UUID"""
        if not self.is_valid_user(id):

            self._loaded_data = PlayerData()

        else:

            result = self.http_client.request(
                method="GET",
                url=self.DATA_API,
                fields=self.__fields(),
                headers=self.headers,
            )

            self._loaded_data = PlayerData.from_dict(self.jsonify(result.data))

        self.log_action(id, self.read_data.uuid, "Player Data")

    def load_friends(self, id: str) -> None:
        """Loads a player's friends list by account name or UUID"""
        if not self.is_valid_user(id):

            self._loaded_friends = PlayerFriends()

        else:

            result = self.http_client.request(
                method="GET",
                url=self.FRIENDS_API,
                fields=self.__fields(),
                headers=self.headers,
            )

            self._loaded_friends = PlayerFriends.from_dict(self.jsonify(result.data))

        self.log_action(id, self.read_friends.uuid, "Player Friends")

    def jsonify(self, data: bytes) -> Dict[str, Any]:
        """Translate response bytes to dict, returns empty if fails"""
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def __fields(self) -> Dict[str, str]:
        """Assembles HTTPS fields parameter"""
        return {"uuid": self.user_uuid, "key": self.user_apikey}
