# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""
import yaml
import re
from netmiko import ConnectHandler
from pprint import pprint

# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]
commands = commands_with_errors + correct_commands

def send_config_commands(device, config_commands, log=True, choise=True):
    complete = dict()
    errors = dict()
    if log:
        print(f'''Подключение к {device['host']}''')
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        for cmd in commands:
            result = ssh.send_config_set(cmd)
            if '%' not in result:
                complete[cmd] = result
            else:
                errors[cmd] = result
                err = re.search(r'%\s(.+?)\n', result)
                print(f'''Команда "{cmd}" выполнилась с ошибкой "{err.group(1)}" на устройстве {device['host']}''')
                if choise:
                    decide = input('Продолжать выполнять команды? [y]/n: ')
                    if decide != 'n' and decide != 'no':
                        pass
                    else:
                        break
                else:
                    pass
    return(complete, errors)

if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for device in devices:
        pprint(send_config_commands(device, commands))