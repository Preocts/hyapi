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

    RESOLVER_URL = "https://api.mojang.com/users/profiles/minecraft/"
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
        endpoint = self.RESOLVER_URL + name

        result = self.http_client.request(
            "GET",
            endpoint,
        )

        try:
            result_json = json.loads(result.data.decode("utf-8"))
        except json.JSONDecodeError:
            result_json = {}

        return self.LookupResult.from_dict(result_json)
