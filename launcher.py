"""Launcher for running multiple consoles."""
from subprocess import Popen, CREATE_NEW_CONSOLE

PROCESS = []

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break

    elif ACTION == 's':
        PROCESS.append(Popen(['python', 'server'], creationflags=CREATE_NEW_CONSOLE))

        for i in range(1, 3):
            PROCESS.append(Popen(f'python client -n user_{i} -m send -n noname', creationflags=CREATE_NEW_CONSOLE))

        for _ in range(3):
            PROCESS.append(Popen('python client', creationflags=CREATE_NEW_CONSOLE))

    if ACTION == 'q' or ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
