"""
Base class for authorization and player lookup

Author: Preocts <Preocts#8196>
"""
import logging

from hyapi.utils import is_valid_java_name
from hyapi.utils import is_valid_uuid
from hyapi.uuidlookup import UUIDLookup
from secretbox.loadenv import LoadEnv


class AuthUser:
    """User authorization and lookup"""

    logger = logging.getLogger("AuthUser")
    uuid_client = UUIDLookup()

    def __init__(self) -> None:
        """On initialization, pulls API key from .env file"""
        secrets = LoadEnv(auto_load=True)
        self.user_uuid = ""
        self.user_name = ""
        self.user_apikey = secrets.get("HYAPI_APIKEY")
        if not self.user_apikey:
            self.logger.critical("Missing environment var: HYAPI_APIKEY")
            raise ValueError("Missing 'HYAPI_APIKEY'.")

    def is_valid_user(self, id: str) -> bool:
        """Validates user uuid, if name then looks up UUID"""
        if not is_valid_uuid(id):

            if is_valid_java_name(id):

                self.logger.debug("Resolving by name: %s", id)
                result = self.uuid_client.resolve_by_name(id)

            else:

                raise ValueError(f"Invalid id provided: '{id}'")

        else:

            self.logger.debug("Resolving by uuid: %s", id)
            result = self.uuid_client.resolve_by_uuid(id)

        self.logger.info("Validation result: %s", result)
        self.user_uuid = result.id if result.id else ""
        self.user_name = result.name if result.name else ""

        return bool(self.user_uuid)
