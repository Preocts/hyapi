"""Utility functions"""
import re

DASHED_UUID = r"^[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}$"
UUID = r"^[0-9a-f]{32}$"


def is_valid_uuid(uuid: str) -> bool:
    """Is the uuid valid"""
    return bool(re.search(DASHED_UUID, uuid)) or bool(re.search(UUID, uuid))
