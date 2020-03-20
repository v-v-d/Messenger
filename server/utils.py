"""Server side utility functions for Messenger app."""
from argparse import ArgumentParser
from collections import namedtuple

import yaml

from db.settings import DEFAULT_DB_CONNECTION_URL
from settings import PATH_TO_CONFIG_FILE, DEFAULT_ADDRESS, DEFAULT_PORT


def parse_args(*args):
    """
    Create a command line argument parser and add arguments to it.
    :param (Tuple) args: Tuple with arguments for parser.
    :return (argparse.Namespace): Namespace with added arguments.
    """
    parser = ArgumentParser(description='Set up server parameters.')
    parser.add_argument(
        '-a', '--address', type=str,
        required=False, help='Set server IP address'
    )
    parser.add_argument(
        '-p', '--port', type=int,
        required=False, help='Set server listening port'
    )
    parser.add_argument(
        '-m', '--migrate', action='store_true',
        required=False, help='Propagate changes into database'
    )
    parser.add_argument(
        '-c', '--config', type=str,
        required=False, help='Sets config file path'
    )
    return parser.parse_args(*args)


def get_config(parser):
    Config = namedtuple('Config', ['address', 'port', 'db_connection_url'])
    config = Config(DEFAULT_ADDRESS, DEFAULT_PORT, DEFAULT_DB_CONNECTION_URL)

    if parser.address:
        config = config._replace(address=parser.address)
    if parser.port:
        config = config._replace(port=parser.port)

    if parser.config:
        file_config = get_config_from_yaml(filename=parser.config)
    else:
        file_config = get_config_from_yaml()

    if file_config:
        file_config_addr, file_config_port = file_config.get('host'), file_config.get('port')
        if file_config_addr:
            config = config._replace(address=file_config_addr)
        if file_config_port:
            config = config._replace(port=file_config_port)

        db_path, db_file = file_config.get('db_path'), file_config.get('db_file')
        if db_path and db_file:
            config = config._replace(db_connection_url=f'sqlite:///{db_path}/{db_file}')

    return config


def get_config_from_yaml(filename=PATH_TO_CONFIG_FILE):
    try:
        with open(filename, encoding='UTF-8') as file:
            return yaml.load(file, Loader=yaml.Loader)

    except IOError:
        pass


def write_config_to_yaml(data, filename=PATH_TO_CONFIG_FILE):
    with open(filename, 'w', encoding='UTF-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)


def get_socket_info(addr, port):
    Socket_info = namedtuple('Socket_info', ['addr', 'port'])
    return Socket_info(addr, port)


def get_receiver_addr_and_port(protocol_object):
    remote_socket_info = protocol_object.get('address').get('remote')
    return remote_socket_info.get('addr'), remote_socket_info.get('port')
