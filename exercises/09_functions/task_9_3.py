# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map(config_filename):
    with open(config_filename) as file:
        config_one_str = file.read()
        config_list = config_one_str.split('interface ')
        result_list = list()
        access_dict = dict()
        trunk_dict = dict()
    for elem in config_list:
        if 'access' in elem or 'trunk' in elem:
            result_list.append(elem)
    for elem in result_list:
        if 'mode access' in elem:
            intf_cfg_list = elem.split('\n')
            for line in intf_cfg_list:
                if 'access vlan' in line:
                    vlan = line.split()[-1]
            access_dict[intf_cfg_list[0]] = int(vlan)
        elif 'mode trunk' in elem:
            intf_cfg_list = elem.split('\n')
            for line in intf_cfg_list:
                if 'trunk allowed vlan' in line:
                    vlan_list_str = line.split()[-1].split(',')
                    vlan_list_int = [ int(elem) for elem in vlan_list_str ]
            trunk_dict[intf_cfg_list[0]] = vlan_list_int
    list_for_tupple = [access_dict, trunk_dict] 

    return tuple(list_for_tupple)

print(get_int_vlan_map('config_sw1.txt'))