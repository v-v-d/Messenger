"""Server side database settings for Messenger app."""
import os

import settings

BASE_DIR = os.path.dirname(__file__)

DB_CONNECTION_URL = f'sqlite:///{BASE_DIR}/default.db'

DEFAULT_SECRET_KEY = 'zp5bK7Ah'

SECRET_KEY = getattr(settings, 'SECRET_KEY', DEFAULT_SECRET_KEY)
