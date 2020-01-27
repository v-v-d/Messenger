"""Tests for server make_response Server class method."""
from time import time

import pytest

from app import Server


@pytest.fixture
def server_fixture():
    """
    Server instance fixture.
    :return (<class 'app.Server'>): Server instance.
    """
    return Server()


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


def test_valid_make_response(server_fixture, valid_request_fixture):
    """Test that method returns response with 200 status code."""
    response = server_fixture.make_response(valid_request_fixture)
    assert response.get('status') == 200


def test_invalid_make_response(server_fixture, invalid_request_fixture):
    """Test that method returns response with 400 status code."""
    response = server_fixture.make_response(invalid_request_fixture)
    assert response.get('status') == 400
