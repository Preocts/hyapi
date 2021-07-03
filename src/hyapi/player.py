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
from hyapi.models.playergames import PlayerGames
from hyapi.models.playerstatus import PlayerStatus


class Player(AuthUser):
    """Player object"""

    DATA_API = "https://api.hypixel.net/player"
    FRIENDS_API = "https://api.hypixel.net/friends"
    GAMES_API = "https://api.hypixel.net/recentgames"
    STATUS_API = "https://api.hypixel.net/status"

    logger = logging.getLogger("Player")

    def __init__(self) -> None:
        """Creates an instance of the player class"""
        super().__init__()

        self.http_client = urllib3.PoolManager(retries=urllib3.Retry(total=2))
        self.headers = {"Accept": "application/json"}

        self._data = PlayerData()
        self._friends = PlayerFriends()
        self._games = PlayerGames()
        self._status = PlayerStatus()

    @property
    def read_data(self) -> PlayerData:
        """Player's Game Data"""
        return self._data

    @property
    def read_friends(self) -> PlayerFriends:
        """Player's Friends"""
        return self._friends

    @property
    def read_games(self) -> PlayerGames:
        """Player's recently played games"""
        return self._games

    @property
    def read_status(self) -> PlayerStatus:
        """Player's recent status"""
        return self._status

    def fetch_player(self, player_id: str) -> None:
        """Pulls information on a player by current displayname or UUID"""
        valid = self.is_valid_user(player_id)

        self._data = self._load_data(player_id) if valid else PlayerData()
        self._friends = self._load_friends(player_id) if valid else PlayerFriends()
        self._games = self._load_games(player_id) if valid else PlayerGames()
        self._status = self._load_status(player_id) if valid else PlayerStatus()

    def _log_action(self, id: str, uuid: str, obj: str) -> None:
        """Logger"""
        if uuid:
            self.logger.info("%s loaded for: '%s'", obj, uuid)
        else:
            self.logger.warning("Could not load %s for: '%s'", obj, id)

    def _load_data(self, id: str) -> PlayerData:
        """Loads a player data"""

        result = self._get(self.DATA_API)

        data = PlayerData.from_dict(self._jsonify(result.data))

        self._log_action(id, self.read_data.uuid, "Player Data")

        return data

    def _load_friends(self, id: str) -> PlayerFriends:
        """Loads a player's friends"""

        result = self._get(self.FRIENDS_API)

        friends = PlayerFriends.from_dict(self._jsonify(result.data))

        self._log_action(id, self.read_friends.uuid, "Player Friends")

        return friends

    def _load_games(self, id: str) -> PlayerGames:
        """Loads a player's recent games"""

        result = self._get(self.GAMES_API)

        games = PlayerGames.from_dict(self._jsonify(result.data))

        self._log_action(id, self.read_friends.uuid, "Player Recent Games")

        return games

    def _load_status(self, id: str) -> PlayerStatus:
        """Loads a player's status"""

        result = self._get(self.STATUS_API)

        status = PlayerStatus.from_dict(self._jsonify(result.data))

        self._log_action(id, self.read_friends.uuid, "Player Status")

        return status

    def _jsonify(self, data: bytes) -> Dict[str, Any]:
        """Translate response bytes to dict, returns empty if fails"""
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _fields(self) -> Dict[str, str]:
        """Assembles HTTPS fields parameter"""
        return {"uuid": self.user_uuid, "key": self.user_apikey}

    def _get(self, route: str) -> Any:
        """HTTPS GET from given API route"""
        return self.http_client.request(
            method="GET",
            url=route,
            fields=self._fields(),
            headers=self.headers,
        )
