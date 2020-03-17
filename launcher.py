"""Launcher for running multiple consoles."""
from subprocess import Popen, CREATE_NEW_CONSOLE


PROCESSES = []


def print_help():
    print('h - help')
    print('q - quit')
    print('s - run server')
    print('k - run clients')
    print('x - close all windows')


def quit_from_launcher():
    return True


def start_server():
    PROCESSES.append(Popen(['py', '-3', 'server', '-m'], creationflags=CREATE_NEW_CONSOLE))


def start_clients():
    clients_qty = int(input('How many clients you want to start: '))

    for i in range(clients_qty):
        PROCESSES.append(Popen(
            ['py', '-3', 'client', '-n', f'client_{i}', '-m'],
            creationflags=CREATE_NEW_CONSOLE)
        )


def kill_processes():
    while PROCESSES:
        victim = PROCESSES.pop()
        victim.kill()


MENU = {
    'h': print_help,
    'q': quit_from_launcher,
    's': start_server,
    'k': start_clients,
    'x': kill_processes,
}

print('Enter action. "h" for help.')

while True:
    ACTION = input()

    if MENU.get(ACTION):
        IS_CLOSED = MENU[ACTION]()
        if IS_CLOSED:
            break
    else:
        print('Action not supported. Enter "h" for help.')
