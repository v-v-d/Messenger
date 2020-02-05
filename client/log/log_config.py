"""Basic configuration for the client logging system."""
import os

from settings import DEBUG


FILENAME = 'client.log'
CURRENT_PATH = os.path.dirname(os.path.relpath(__file__))
FILE_PATH = os.path.join(CURRENT_PATH, FILENAME)

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        },
        'decorator': {
            'format': '%(asctime)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': FILE_PATH,
            'encoding': 'UTF-8',
        },
        'decorator': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'decorator',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'client': {
            'handlers': ['console', 'file'] if DEBUG else ['file'],
            'level': 'DEBUG',
        },
        'decorators': {
            'handlers': ['decorator'] if DEBUG else [],
            'level': 'DEBUG',
        },
    },
}
