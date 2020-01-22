"""Tests for client get_socket_params utility function."""
from argparse import Namespace

import pytest

from utils import get_socket_params


@pytest.fixture
def address_fixture():
    """Client IP address fixture.
    :return (tuple): Tuple with IP address key and value for command line.
    """
    return '-a', '127.0.0.1'


@pytest.fixture
def port_fixture():
    """
    Server listening port fixture.
    :return (tuple): Tuple with port key and value for command line.
    """
    return '-p', '8888'


@pytest.fixture
def invalid_port_fixture():
    """
    Invalid server listening port fixture.
    :return (tuple): Tuple with port key and value for command line.
    """
    return '-p', '10'


def test_valid_get_socket_params(address_fixture, port_fixture):
    """Test that function returns argparse.Namespace type namespace when valid args are passed."""
    socket_params = get_socket_params((*address_fixture, *port_fixture))
    assert type(socket_params) == Namespace


def test_invalid_get_socket_params(address_fixture, invalid_port_fixture):
    """Test that function raises ValueError when invalid port passed."""
    with pytest.raises(ValueError):
        get_socket_params((*address_fixture, *invalid_port_fixture))
