# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
from netmiko import ConnectHandler
from textfsm import clitable
import yaml

def send_and_parse_show_command(device_dict, command, index_file='index', templates_path='templates'):
    attributes = {'Command': command,
                  'Vendor': 'cisco_ios'}
    with ConnectHandler(**device_dict) as ssh:
        output = ssh.send_command(command)
    result = list()
    cli_table_obj = clitable.CliTable(index_file, templates_path)
    cli_table_obj.ParseCmd(output, attributes)
    header = list(cli_table_obj.header)
    length = len(header)
    for elem in cli_table_obj:
        temp_dict = dict.fromkeys(header)
        counter = 0
        while counter < length:
          temp_dict[header[counter]] = elem[counter]
          counter += 1
        result.append(temp_dict)
    return(result)    

if __name__ == "__main__":
    command = 'sh ip int br'
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    print(send_and_parse_show_command(devices[0], command))