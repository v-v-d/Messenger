"""Tests for client is_port_valid utility function."""
import pytest

from utils import is_port_valid


@pytest.fixture
def valid_port_fixture():
    """
    Valid server listening port fixture.
    :return (int): Server listening port.
    """
    return 8888


@pytest.fixture
def invalid_port_fixture():
    """
    Invalid server listening port fixture.
    :return (int): Server listening port.
    """
    return 10


def test_valid_is_port_valid(valid_port_fixture):
    """Test that function returns True when valid port passed."""
    assert is_port_valid(valid_port_fixture)


def test_invalid_is_port_valid(invalid_port_fixture):
    """Test that function returns False when invalid port passed."""
    assert not is_port_valid(invalid_port_fixture)
