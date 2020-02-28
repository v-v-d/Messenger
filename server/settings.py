"""Settings for server side of Messenger app. """
import os

BASE_DIR = os.path.dirname(__file__)

CONFIG_FILENAME = 'config.yml'

PATH_TO_CONFIG_FILE = os.path.join(BASE_DIR, CONFIG_FILENAME)

DEFAULT_ADDRESS = '0.0.0.0'

DEFAULT_PORT = 9999

DEBUG = False
