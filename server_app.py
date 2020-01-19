"""Messenger server side main script."""
import sys

from server import Server


LISTEN_PORT = None
LISTEN_ADDRESS = None

try:
    if '-p' in sys.argv:
        LISTEN_PORT = int(sys.argv[sys.argv.index('-p') + 1])
        if not 1024 < LISTEN_PORT < 65535:
            raise ValueError
except IndexError:
    print('Port number required after key -\'p\'.')
    sys.exit(1)
except ValueError:
    print('Port number must be in range 1024 - 65535.')
    sys.exit(1)

try:
    if '-a' in sys.argv:
        LISTEN_ADDRESS = sys.argv[sys.argv.index('-a') + 1]
except IndexError:
    print('IP address required after key -\'a\'.')
    sys.exit(1)

if LISTEN_ADDRESS and LISTEN_PORT:
    SERVER = Server(host=LISTEN_ADDRESS, port=LISTEN_PORT)
elif LISTEN_ADDRESS:
    SERVER = Server(host=LISTEN_ADDRESS)
elif LISTEN_PORT:
    SERVER = Server(port=LISTEN_PORT)
else:
    print('Listening host and port will be set by default.')
    SERVER = Server()

SERVER.run()
