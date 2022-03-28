# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
vlan_str = input('Введите номер vlan: ')
vlan_int = int(vlan_str)
list_for_strings = list()
list_for_convert = list()
result_list = list()
with open('CAM_table.txt') as file:
    for line in file:
        striped = line.rstrip()
        if striped[1:2].isdigit():
            tmp_list = striped.split()
            list_for_strings.append(f'''{tmp_list[0]:10}{tmp_list[1]:20}{tmp_list[3]:5}''')
            #list_for_strings.append(int(tmp_list[0]), f'''{tmp_list[0]:10}{tmp_list[1]:20}{tmp_list[3]:5}''')
    for elem in list_for_strings:
        list_for_convert.append(elem.split())           
    for elem in list_for_convert:
        result_sublist = list()
        result_sublist.append(int(elem[0]))
        result_sublist.append(elem[1])
        result_sublist.append(elem[2])
        result_list.append(result_sublist)
result = sorted(result_list)
for elem in result:
    if elem[0] == vlan_int:
        print(f'''{elem[0]:<10}{elem[1]:20}{elem[2]:5}''')
