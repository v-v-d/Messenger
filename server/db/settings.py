"""Server side database settings for Messenger app."""
import os

BASE_DIR = os.path.dirname(__file__)

DB_CONNECTION_URL = f'sqlite:///{BASE_DIR}/default.db'
