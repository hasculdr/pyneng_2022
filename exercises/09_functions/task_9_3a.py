# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

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
            if 'access vlan' in elem:
                for line in intf_cfg_list:
                    if 'access vlan' in line:
                        vlan = line.split()[-1]
                access_dict[intf_cfg_list[0]] = int(vlan)
            elif 'access vlan' not in elem:
                access_dict[intf_cfg_list[0]] = 1
        elif 'mode trunk' in elem:
            intf_cfg_list = elem.split('\n')
            for line in intf_cfg_list:
                if 'trunk allowed vlan' in line:
                    vlan_list_str = line.split()[-1].split(',')
                    vlan_list_int = [ int(elem) for elem in vlan_list_str ]
            trunk_dict[intf_cfg_list[0]] = vlan_list_int
    list_for_tupple = [access_dict, trunk_dict] 

    return tuple(list_for_tupple)

print(get_int_vlan_map('config_sw2.txt'))