"""Decorators for Messenger server side."""
import json
import zlib
from functools import wraps
from inspect import currentframe
from logging import getLogger
from logging.config import dictConfig

from db.database import session_scope

from db.models import ClientSession
from log.log_config import LOGGING
from protocol import make_response

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


def login_required(func):
    """Check that user is logged in based on the valid token exists in request."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if 'token' not in request:
            return make_response(request, 401, 'Valid authentication credentials lack')

        with session_scope() as session:
            client_session = session.query(ClientSession).filter_by(token=request.get('token')).first()
            if not client_session or client_session.closed:
                return make_response(request, 403, 'Access denied')

        return func(request, *args, **kwargs)
    return wrapper


def compression_middleware(func):
    """Decompress request and return compression result."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)
    return wrapper


def json_middleware(func):
    """Load bytes JSON to dict and return bytes JSON."""
    @wraps(func)
    def wrapper(raw_request, *args, **kwargs):
        request = json.loads(raw_request.decode('UTF-8'))
        LOGGER.debug(f'Client send request: {request}.')
        response = func(request, *args, **kwargs)
        return json.dumps(response).encode('UTF-8')
    return wrapper
