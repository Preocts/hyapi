"""Unit tests for authuser.py"""
import os
from typing import Generator
from unittest.mock import patch

import pytest
import vcr
from hyapi.authuser import AuthUser
from hyapi.authuser import SecretBox

TEST_NAME = "jeb"
TEST_UUID = "f498513c-e8c8-4773-be26-ecfc7ed5185d"
INVALID_NAME = "wellthistotallyisn'tgoing towork"
RECORDING_MODE = False

recorder = vcr.VCR(
    serializer="yaml",
    cassette_library_dir="tests/fixtures",
    record_mode="new_episodes" if RECORDING_MODE else "once",
    match_on=["uri", "method"],
)


@pytest.fixture(scope="function", name="auth")
def fixture_auth() -> Generator[AuthUser, None, None]:
    """Build a fixure"""
    with recorder.use_cassette("vcr_authuser.yaml"):

        with patch.dict(os.environ, {"HYAPI_APIKEY": "mock"}):

            auth = AuthUser()

            yield auth


def test_uuid(auth: AuthUser) -> None:
    """Valid UUID"""

    assert auth.is_valid_user(TEST_UUID)
    assert auth.user_uuid
    assert auth.user_name


def test_name(auth: AuthUser) -> None:
    """Valid Name, no UUID"""

    assert auth.is_valid_user(TEST_NAME)
    assert auth.user_uuid
    assert auth.user_name


def test_invalid_id(auth: AuthUser) -> None:
    """Invalid will raise"""

    with pytest.raises(ValueError):
        auth.is_valid_user(INVALID_NAME)


def test_missing_api_key() -> None:
    with patch.object(SecretBox, "get", return_value=""):

        with pytest.raises(ValueError):

            _ = AuthUser()
