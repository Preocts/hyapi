"""
Player object

Author: Preocts <Preocts#8196>
"""
from typing import Optional

from hyapi.utils import is_valid_java_name
from hyapi.utils import is_valid_uuid
from hyapi.uuidlookup import UUIDLookup
from secretbox.loadenv import LoadEnv


class Player:
    """Player object"""

    lookup = UUIDLookup()

    def __init__(
        self,
        uuid: Optional[str] = None,
        mc_name: Optional[str] = None,
    ) -> None:
        """
        Creates an instance of the player class, at least one arg is required

        Args:
            uuid: [optional] Your minecraft UUID
            mc_name: [optional] Your minecraft player name (for UUID lookup)

        """
        self._secrets = LoadEnv(auto_load=True)
        self.uuid = uuid
        self.mc_name = mc_name

        if self.uuid is not None and not is_valid_uuid(self.uuid):
            raise ValueError("Invalid UUID provided")

        if self.mc_name is not None and not is_valid_java_name(self.mc_name):
            raise ValueError("Invalid Java Minecraft name provided")

        elif self.uuid is None and self.mc_name is not None:
            self.uuid = self.lookup.resolve_by_name(self.mc_name).id

        if self.uuid is None:
            raise ValueError("Unable to resolve UUID")
