# -*- coding: utf-8 -*-
"""
Задание 5.3a

Дополнить скрипт из задания 5.3 таким образом, чтобы, в зависимости
от выбранного режима, задавались разные вопросы в запросе о номере
VLANа или списка VLANов:
* для access: 'Введите номер VLAN:'
* для trunk: 'Введите разрешенные VLANы:'

Ограничение: Все задания надо выполнять используя только пройденные темы.
То есть эту задачу можно решить без использования условия if и циклов for/while.
"""

access_template = [
    "switchport mode access",
    "switchport access vlan {}",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
]

trunk_template = [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk allowed vlan {}",
]
switchport_mode = input('Введите режим работы интерфейса (access/trunk): ')
interface = input('Введите тип и номер интерфейса: ')

vlans_dict = dict(access = 'Введите номер VLAN: ', trunk = 'Введите разрешенные VLANы: ')
vlans = input(vlans_dict[switchport_mode])

access_dict = dict.fromkeys(access_template)
trunk_dict = dict.fromkeys(trunk_template)
templates = dict(access = access_dict, trunk = trunk_dict)
temp_var = list(templates[switchport_mode].keys())
temp_var2 = ','.join(temp_var)
temp_var3 = temp_var2.replace(',', '\n')
print(f'''interface {interface}''')
print(temp_var3.format(vlans))