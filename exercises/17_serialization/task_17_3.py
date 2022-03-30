# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re
from pprint import pprint

def parse_sh_cdp_neighbors(string):
    hostname = re.search(r'(\S+)[>#]', string)
    neighbors_reg = re.compile(r'(?P<remote_device>\w+)\s+'
                               r'(?P<local_int>\w+\s\S+)\s+'
                               r'\d+\s+(?:\w\s)+\s+\S+\s+'
                               r'(?P<remote_int>\w+\s\S+)')
    neighbors_data_list = string.split('\n')
    subdict = dict()
    result_dict = dict()
    for line in neighbors_data_list:
        match = neighbors_reg.search(line)
        if match:
                key = match.group('local_int')
                sub_key = match.group('remote_device')
                sub_value = match.group('remote_int')
                subdict[key] = {sub_key: sub_value}
                result_dict[hostname.group(1)] = subdict
    return (result_dict)

if __name__ == '__main__':
    with open('sh_cdp_n_r2.txt') as file:
        string = file.read()
    pprint(parse_sh_cdp_neighbors(string))