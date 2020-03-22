"""Launcher for running multiple consoles."""
from subprocess import Popen, CREATE_NEW_CONSOLE


PROCESSES = []


def print_help():
    print('h - help')
    print('q - quit')
    print('s - run server')
    print('c - run client')
    print('x - close all windows')


def quit_from_launcher():
    return True


def start_server():
    PROCESSES.append(Popen(
        ['py', '-3', 'server', '-m'],
        creationflags=CREATE_NEW_CONSOLE)
    )


def start_client():
    PROCESSES.append(Popen(
        ['py', '-3', 'client', '-a', '192.168.0.107', '-p', '8080'],
        creationflags=CREATE_NEW_CONSOLE)
    )


def kill_processes():
    while PROCESSES:
        victim = PROCESSES.pop()
        victim.kill()


RESOLVER = {
    'h': print_help,
    'q': quit_from_launcher,
    's': start_server,
    'c': start_client,
    'x': kill_processes,
}

print('Welcome to launcher. Enter "h" for help.')

while True:
    ACTION = input('Enter action ("h" for help): ')

    if RESOLVER.get(ACTION):
        IS_CLOSED = RESOLVER[ACTION]()
        if IS_CLOSED:
            break
    else:
        print('Action not supported. Enter "h" for help.')
