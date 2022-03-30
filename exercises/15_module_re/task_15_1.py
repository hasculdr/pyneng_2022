# -*- coding: utf-8 -*-
"""
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.


Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re
from pprint import pprint

def get_ip_from_cfg(filename):
    with open(filename) as file:
        config_list = file.readlines()
    regex = re.compile(r'.+?address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)')
    matches = list()
    for line in config_list:
        match_obj = regex.search(line)
        if match_obj:
            matches.append(match_obj.groups())
    return(matches)

if __name__ == '__main__':
    pprint(get_ip_from_cfg('config_r1.txt'))