"""Unit tests for authuser.py"""
from typing import Generator
from unittest.mock import patch

import pytest
import vcr
from hyapi.authuser import AuthUser

TEST_NAME = "jeb"
TEST_UUID = "f498513c-e8c8-4773-be26-ecfc7ed5185d"
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

        auth = AuthUser()

        yield auth


def test_uuid_no_name(auth: AuthUser) -> None:
    """Valid UUID, no name"""
    auth.user_uuid = TEST_UUID
    auth.user_name = ""

    assert auth.is_valid_user
    assert auth.user_name


def test_name_no_uuid(auth: AuthUser) -> None:
    """Valid Name, no UUID"""
    auth.user_uuid = TEST_NAME
    auth.user_name = ""

    assert auth.is_valid_user
    assert auth.user_name


def test_invalid_uuid(auth: AuthUser) -> None:
    """Invalid will raise"""
    auth.user_uuid = "wellthistotallyisn'tgoing towork"

    with pytest.raises(ValueError):
        auth.is_valid_user


def test_static_value(auth: AuthUser) -> None:
    """Once we validate, don't re-validate same object"""
    with patch.object(auth, "_validate_user", return_value=False) as patched:
        assert not auth.is_valid_user
        assert not auth.is_valid_user

        assert patched.call_count == 1
