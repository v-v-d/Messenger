"""Messenger server side main script."""
import sys

from server import Server


listen_port = None
listen_address = None

try:
    if '-p' in sys.argv:
        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        if not 1024 < listen_port < 65535:
            raise ValueError
except IndexError:
    print('Port number required after key -\'p\'.')
    sys.exit(1)
except ValueError:
    print('Port number must be in range 1024 - 65535.')
    sys.exit(1)

try:
    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
except IndexError:
    print('IP address required after key -\'a\'.')
    sys.exit(1)

if listen_address and listen_port:
    server = Server(host=listen_address, port=listen_port)
elif listen_address:
    server = Server(host=listen_address)
elif listen_port:
    server = Server(port=listen_port)
else:
    print('Listening host and port will be set by default.')
    server = Server()

server.run()
