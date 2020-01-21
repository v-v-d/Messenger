"""Tests for client is_response_valid Client class method."""
import pytest

from app import Client


@pytest.fixture
def valid_response_fixture():
    """Valid response fixture.
    :return (dict): Dict with valid response.
    """
    return {'status': 200}


@pytest.fixture
def invalid_response_fixture():
    """Valid response fixture.
    :return (dict): Dict with invalid response.
    """
    return {}


def test_valid_is_response_valid(valid_response_fixture):
    """Test that method returns True when valid response passed."""
    assert Client.is_response_valid(valid_response_fixture)


def test_invalid_is_response_valid(invalid_response_fixture):
    """Test that method raises ValueError when invalid response passed."""
    with pytest.raises(ValueError):
        Client.is_response_valid(invalid_response_fixture)
