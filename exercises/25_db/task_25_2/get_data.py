# -*- coding: utf-8 -*-

from sys import argv
from pprint import pprint
import sqlite3
from tabulate import tabulate


def args_check(argv):
    if len(argv) == 1:
        header = 'В таблице dhcp такие записи:'
        query = 'SELECT * from dhcp'
        return(header, query)
    elif len(argv) == 3:
        header = f"Информация об устройствах с такими параметрами: {argv[1]} {argv[2]}\n"
        query = f"SELECT * from dhcp WHERE {argv[1]} = '{argv[2]}'"
        return(header, query)
    else:
        return False

def get_data(header, query):
    connection = sqlite3.connect('dhcp_snooping.db')
    try:
        data = connection.execute(query)
        result = tabulate(data)
        connection.close()
        print(header, result)
    except sqlite3.OperationalError:
        print('Данный параметр не поддерживается. '
              'Допустимые значения параметров: mac, ip, vlan, interface, switch')


if __name__ == '__main__':
    if args_check(argv):
        tmp = args_check(argv)
        get_data(tmp[0], tmp[1])
    else:
        print('Пожалуйста, введите два или ноль аргументов')