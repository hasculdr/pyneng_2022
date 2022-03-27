# -*- coding: utf-8 -*-
"""
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.
"""

ospf_route = "      10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
ospf_data_list = ospf_route.split()

result = dict()
result['Prefix'] = ospf_data_list[0]
result['AD/Metric'] = ospf_data_list[1].strip('[]')
result['Next-Hop'] = ospf_data_list[3].strip(',')
result['Last update'] = ospf_data_list[4].strip(',')
result['Outbound Interface'] = ospf_data_list[5]

print(f'''
    {"Prefix":<22}{result['Prefix']:<15}
    {"AD/Metric":<22}{result['AD/Metric']:<15}
    {"Next-Hop":<22}{result['Next-Hop']:<15}
    {"Last update":<22}{result['Last update']:<15}
    {"Outbound Interface":<22}{result['Outbound Interface']:<15}''')