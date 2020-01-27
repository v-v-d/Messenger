"""Tests for server is_request_valid Server class method."""
from time import time

import pytest

from app import Server


@pytest.fixture
def valid_request_fixture():
    """Valid request fixture.
    :return (dict): Dict with valid request.
    """
    return {
        'action': 'presence',
        'time': time(),
        'user': {
            'account_name': 'Guest'
        }
    }


@pytest.fixture
def invalid_request_fixture():
    """Valid request fixture.
    :return (dict): Dict with invalid request.
    """
    return {}


def test_valid_is_request_valid(valid_request_fixture):
    """Test that method returns True when valid request passed."""
    assert Server.is_request_valid(valid_request_fixture)


def test_invalid_is_response_valid(invalid_request_fixture):
    """Test that method returns False when valid request passed."""
    assert not Server.is_request_valid(invalid_request_fixture)
