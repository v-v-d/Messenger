"""Server side database settings for Messenger app."""
import os

import settings

BASE_DIR = os.path.dirname(__file__)

DEFAULT_DB_URL = f'{BASE_DIR}/default.db'

DEFAULT_DB_CONNECTION_URL = f'sqlite:///{DEFAULT_DB_URL}'

DEFAULT_SECRET_KEY = 'zp5bK7Ah'

SECRET_KEY = getattr(settings, 'SECRET_KEY', DEFAULT_SECRET_KEY)
