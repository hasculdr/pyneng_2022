# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""
from pprint import pprint

#ip_list = ["10.1.1.1", "10.4.10.10-13", "192.168.1.12-192.168.1.15"]
ip_list = ['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

def convert_ranges_to_ip_list(ip_list):
    verbose_list = list()
    for elem in ip_list:
        if '-' not in elem:
            verbose_list.append(elem)
        else:
            start, end = elem.split('-')
            first, second, third, fourth_start = start.split('.')
            verbose_list.append(start)
            if len(end) > 3:
                *trash, fourth_end = end.split('.')
                for num in range(int(fourth_start)+1, int(fourth_end)+1):
                    verbose_list.append(f'{first}.{second}.{third}.{num}')
            else:
                for num in range(int(fourth_start)+1, int(end)+1):
                    verbose_list.append(f'{first}.{second}.{third}.{num}')
    return(verbose_list)

if __name__ == '__main__':
    print(convert_ranges_to_ip_list(ip_list))