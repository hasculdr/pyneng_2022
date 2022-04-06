# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""
from textfsm import clitable

def parse_command_dynamic(command_output, attributes_dict, index_file='index', templ_path='templates'):
    result = list()
    cli_table_obj = clitable.CliTable(index_file, templ_path)
    cli_table_obj.ParseCmd(command_output, attributes_dict)
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
    attributes = {'Command': 'show ip interface brief',
                  'Vendor': 'cisco_ios'
    }
    with open('output/sh_ip_int_br.txt') as output_obj:
        output = output_obj.read()
        print(parse_command_dynamic(output, attributes))