"""
Looks up UUID from player name

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


class UUIDLookup:
    """Look up service for UUID from player name"""

    NAME_RESOLVER_URL = "https://api.mojang.com/users/profiles/minecraft/"
    UUID_RESOLVER_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"

    logger = logging.getLogger(__name__)

    class LookupResult(NamedTuple):
        """Results of a lookup"""

        id: Optional[str]
        name: Optional[str]
        legacy: bool = False
        demo: bool = False

        @classmethod
        def from_dict(cls, data: Dict[str, Any]) -> UUIDLookup.LookupResult:
            """Create object from dict"""
            return cls(
                id=data.get("id"),
                name=data.get("name"),
                legacy=data.get("legacy", False),
                demo=data.get("demo", False),
            )

    def __init__(self) -> None:
        """Creates a thread safe client for UUID lookup"""
        self.http_client = urllib3.PoolManager(
            retries=urllib3.Retry(5, redirect=None, backoff_factor=0.1)
        )

    def resolve_by_name(self, name: str) -> LookupResult:
        """Resolve a player name to UUID"""

        self.logger.debug("Resolving name: '%s'", name)

        result = self.http_client.request("GET", self.NAME_RESOLVER_URL + name)

        return self.__parse_resolver_data(result.data.decode("utf-8"))

    def resolve_by_uuid(self, uuid: str) -> LookupResult:
        """Resolve a player UUID to name"""

        self.logger.debug("Resolving uuid: '%s'", uuid)

        result = self.http_client.request("GET", self.UUID_RESOLVER_URL + uuid)

        return self.__parse_resolver_data(result.data.decode("utf-8"))

    def __parse_resolver_data(self, data: str) -> LookupResult:
        """Parase the results of a resolver result"""
        try:
            return self.LookupResult.from_dict(json.loads(data))
        except json.JSONDecodeError:
            return self.LookupResult.from_dict({})
