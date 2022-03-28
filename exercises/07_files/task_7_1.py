# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
with open('ospf.txt') as file:
    ospf_data = list()
    for line in file:
        ospf_data.append(line.split())
    for sub_list in ospf_data:
        print(f'''{"Prefix":20}{sub_list[1]:<15}\n'''
              f'''{"AD/Metric":20}{sub_list[2].strip('[]'):<15}\n'''
              f'''{"Next-Hop":20}{sub_list[4].rstrip(','):<15}\n'''
              f'''{"Last update":20}{sub_list[5].rstrip(','):<15}\n'''
              f'''{"Outbound Interface":20}{sub_list[6]:<15}''')