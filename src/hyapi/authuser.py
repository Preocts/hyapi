import logging
from typing import Optional

from hyapi.utils import is_valid_java_name
from hyapi.utils import is_valid_uuid
from hyapi.uuidlookup import UUIDLookup
from secretbox.loadenv import LoadEnv


class AuthUser:
    """User authorization and authentication"""

    logger = logging.getLogger("AuthUser")
    uuid_client = UUIDLookup()

    def __init__(self) -> None:
        """On initialization, pulls API key and user's name/uuid from .env file"""
        secrets = LoadEnv(auto_load=True)
        self.user_uuid = secrets.get("HYAPI_USERUUID")
        self.user_name = ""
        self.user_apikey = secrets.get("HYAPI_APIKEY")
        self.__is_valid: Optional[bool] = None

    @property
    def is_valid_user(self) -> bool:
        """Returns true if the HYAPI_USERUUID is valid"""
        if self.__is_valid is None:

            self.__is_valid = self._validate_user()

        return self.__is_valid

    def _validate_user(self) -> bool:
        """Validates HYAPI_USERUUID, if name then looks up UUID"""
        if not is_valid_uuid(self.user_uuid):

            if is_valid_java_name(self.user_uuid):

                result = self.uuid_client.resolve_by_name(self.user_uuid)

            else:

                raise ValueError(f"Invalid 'HYAPI_USERUUID': '{self.user_uuid}'")

        else:

            result = self.uuid_client.resolve_by_uuid(self.user_uuid)

        self.user_uuid = result.id if result.id else ""
        self.user_name = result.name if result.name else ""

        return bool(self.user_uuid)
