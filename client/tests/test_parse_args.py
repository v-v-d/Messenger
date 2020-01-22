"""Tests for client parse_args utility function."""
import pytest

from utils import parse_args


@pytest.fixture
def default_address_fixture():
    """Client default IP address fixture.
    :return (str): Client default IP address.
    """
    return 'localhost'


@pytest.fixture
def default_port_fixture():
    """Server default listening port fixture.
    :return (int): Server default listening port.
    """
    return 7777


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


def test_valid_parse_args(address_fixture, port_fixture):
    """Compare passed address and port with returned address and port."""
    parser = parse_args((*address_fixture, *port_fixture))
    assert parser.address == address_fixture[1] and parser.port == int(port_fixture[1])


def test_valid_parse_args_address(address_fixture, default_port_fixture):
    """Compare passed address and default port with returned address and port."""
    parser = parse_args(address_fixture)
    assert parser.address == address_fixture[1] and parser.port == default_port_fixture


def test_valid_parse_args_port(default_address_fixture, port_fixture):
    """Compare default address and passed port with returned address and port."""
    parser = parse_args(port_fixture)
    assert parser.address == default_address_fixture and parser.port == int(port_fixture[1])


def test_valid_parse_args_defaults(default_address_fixture, default_port_fixture, address_fixture, port_fixture):
    """Compare passed and returned address and port with default address and port."""
    parser = parse_args((*address_fixture, *port_fixture))
    assert parser.address != default_address_fixture and parser.port != default_port_fixture
