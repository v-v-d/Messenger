"""Decorations for Messenger server side."""
from functools import wraps
from inspect import currentframe
from logging import getLogger
from logging.config import dictConfig

from log.log_config import LOGGING


dictConfig(LOGGING)
LOGGER = getLogger('decorators')


def log(func):
    """
    Log the passed function name, caller function name and module name
    where the functions is calling. Also args and kwargs are logged too.
    :param (<class 'function'>) func: Handled function.
    :return (<class 'function'>): Decorated function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        f_name = func.__name__
        m_name = func.__module__
        caller = currentframe().f_back.f_code.co_name
        LOGGER.debug(
            f"Function '{f_name}' resolved with: {args}, {kwargs}, called from '{m_name}.py' by '{caller}' function."
        )
        return func(*args, **kwargs)
    return wrapper
    # TODO: Remove the words "function" and make auto detect the type of passed func.
    # TODO: If caller is the same func then func.__module__ return <module>. Needed to fix.
