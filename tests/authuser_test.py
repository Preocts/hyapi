"""Unit tests for authuser.py"""
from unittest.mock import patch

import pytest
from hyapi.authuser import AuthUser

TEST_NAME = "jeb"
TEST_UUID = "f498513c-e8c8-4773-be26-ecfc7ed5185d"


def test_uuid_no_name() -> None:
    """Valid UUID, no name"""
    auth = AuthUser()
    auth.user_uuid = TEST_UUID
    auth.user_name = ""

    assert auth.is_valid_user
    assert auth.user_name


def test_name_no_uuid() -> None:
    """Valid Name, no UUID"""
    auth = AuthUser()
    auth.user_uuid = TEST_NAME
    auth.user_name = ""

    assert auth.is_valid_user
    assert auth.user_name


def test_invalid_uuid() -> None:
    """Invalid will raise"""
    auth = AuthUser()
    auth.user_uuid = "wellthistotallyisn'tgoing towork"

    with pytest.raises(ValueError):
        auth.is_valid_user


def test_static_value() -> None:
    """Once we validate, don't re-validate same object"""
    auth = AuthUser()
    with patch.object(auth, "_validate_user", return_value=False) as patched:
        assert not auth.is_valid_user
        assert not auth.is_valid_user

        assert patched.call_count == 1
