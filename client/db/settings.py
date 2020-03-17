"""Server side database settings for Messenger app."""
import os


BASE_DIR = os.path.dirname(__file__)

# Database settings
DEFAULT_DB_NAME = 'clients'

DEFAULT_DB_CONNECTION_URL = f'sqlite:///{BASE_DIR}/{DEFAULT_DB_NAME}.db'
