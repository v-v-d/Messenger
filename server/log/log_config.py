"""Basic configuration for the server logging system."""
import os


FILENAME = 'server.log'
CURRENT_PATH = os.path.dirname(os.path.relpath(__file__))
FILE_PATH = os.path.join(CURRENT_PATH, FILENAME)

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
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
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': FILE_PATH,
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
            'encoding': 'UTF-8',
        },
    },
    'loggers': {
        'server': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
