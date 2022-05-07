# -*- coding: utf-8 -*-

from sys import argv
import sqlite3
from tabulate import tabulate


def args_check(argv):
    if len(argv) == 1:
        header = 'В таблице dhcp такие записи:'
        act_query = 'SELECT * from dhcp WHERE active = 1'
        inact_query = 'SELECT * from dhcp WHERE active = 0'
        return(header, act_query, inact_query)
    elif len(argv) == 3:
        header = f"Информация об устройствах с такими параметрами: {argv[1]} {argv[2]}\n"
        act_query = f"SELECT * from dhcp WHERE {argv[1]} = '{argv[2]}' AND active = 1"
        inact_query = f"SELECT * from dhcp WHERE {argv[1]} = '{argv[2]}' AND active = 0"
        return(header, act_query, inact_query)
    else:
        return False

def get_data(header, act_query, inact_query):
    act_header = 'Активные записи:'
    inact_header = 'Неактивные записи:'
    connection = sqlite3.connect('dhcp_snooping.db')
    try:
        act_data = connection.execute(act_query)
        inact_data = connection.execute(inact_query)
        act_result = tabulate(act_data)
        inact_result = tabulate(inact_data)
        connection.close()
        if len(act_result) > 0 and len(inact_result) > 0:
            print(header, act_header, act_result, inact_header, inact_result, sep='\n\n')
        elif len(act_result) > 0 and len(inact_result) == 0:
            print(header, act_header, act_result, sep='\n\n')
        elif len(act_result) == 0 and len(inact_result) > 0:
            print(header, inact_header, inact_result, sep='\n\n')
        else:
            print('В таблице dhcp нет записей')
    except sqlite3.OperationalError:
        print('Данный параметр не поддерживается. '
              'Допустимые значения параметров: mac, ip, vlan, interface, switch, active')


if __name__ == '__main__':
    if args_check(argv):
        tmp = args_check(argv)
        get_data(tmp[0], tmp[1], tmp[2])
    else:
        print('Пожалуйста, введите два или ноль аргументов')