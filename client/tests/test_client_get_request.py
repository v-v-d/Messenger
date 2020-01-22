"""Tests for client get_request Client class method."""
from time import time

import pytest

from app import Client


@pytest.fixture
def client_fixture():
    """Client instance fixture.
    :return (Client): Client instance.
    """
    return Client()


@pytest.fixture
def action_fixture():
    """Fixture with action that will be passed to server.
    :return (str): Action.
    """
    return 'presence'


@pytest.fixture
def username_fixture(client_fixture):
    """Username fixture.
    :return (str): Username.
    """
    return client_fixture.name


@pytest.fixture
def request_fixture(action_fixture, username_fixture):
    """Request fixture based on action, time, username.
    :return (dict): Dict with request body.
    """
    return {
        'action': action_fixture,
        'time': time(),
        'user': {
            'account_name': username_fixture
        }
    }


def test_valid_get_request(client_fixture, request_fixture):
    """Test for valid request returned from Client get_request method."""
    request = client_fixture.get_request()
    real_action = request.get('action')
    real_name = request.get('user').get('account_name')
    mock_action = request_fixture.get('action')
    mock_name = request_fixture.get('user').get('account_name')
    assert real_action == mock_action and real_name == mock_name


def test_invalid_get_request(client_fixture):
    """Test for invalid request returned from Client get_request method."""
    request = client_fixture.get_request()
    action = request.get('action')
    name = request.get('user').get('account_name')
    assert action is not None and name is not None
