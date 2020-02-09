"""Launcher for running multiple consoles."""
from subprocess import Popen, CREATE_NEW_CONSOLE

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break

    elif ACTION == 's':
        PROCESS.append(Popen(['python', 'server'], creationflags=CREATE_NEW_CONSOLE))

        for i in range(1, 4):
            PROCESS.append(Popen(f'python client -n user_{i}', creationflags=CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            victim = PROCESS.pop()
            victim.kill()
