"""Server side database settings for Messenger app."""
import os

import settings
from utils import PARSER

BASE_DIR = os.path.dirname(__file__)

# Database settings
DB_NAME = PARSER.name

DB_CONNECTION_URL = f'sqlite:///{BASE_DIR}/{DB_NAME}.db'

