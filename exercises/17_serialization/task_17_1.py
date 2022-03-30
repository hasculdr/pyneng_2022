# -*- coding: utf-8 -*-
"""
Задание 17.1

Создать функцию write_dhcp_snooping_to_csv, которая обрабатывает вывод
команды show dhcp snooping binding из разных файлов и записывает обработанные
данные в csv файл.

Аргументы функции:
* filenames - список с именами файлов с выводом show dhcp snooping binding
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Например, если как аргумент был передан список с одним файлом sw3_dhcp_snooping.txt:
MacAddress          IpAddress        Lease(sec)  Type           VLAN  Interface
------------------  ---------------  ----------  -------------  ----  --------------------
00:E9:BC:3F:A6:50   100.1.1.6        76260       dhcp-snooping   3    FastEthernet0/20
00:E9:22:11:A6:50   100.1.1.7        76260       dhcp-snooping   3    FastEthernet0/21
Total number of bindings: 2

В итоговом csv файле должно быть такое содержимое:
switch,mac,ip,vlan,interface
sw3,00:E9:BC:3F:A6:50,100.1.1.6,3,FastEthernet0/20
sw3,00:E9:22:11:A6:50,100.1.1.7,3,FastEthernet0/21

Первый столбец в csv файле имя коммутатора надо получить из имени файла,
остальные - из содержимого в файлах.

Проверить работу функции на содержимом файлов sw1_dhcp_snooping.txt,
sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt.

"""
import re
import csv

filenames = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']

def write_dhcp_snooping_to_csv(filenames, output):
    hostname = re.compile(r'(?P<host>\w+)_\w+_\w+')
    data_record = re.compile(r'(?P<mac>(?:\w{2}:){5}\w{2})\s+'
                             r'(?P<ip>(?:\d+\.){3}\d+)\s+'
                             r'\d+\s+\S+\s+'
                             r'(?P<vlan>\d+)\s+'
                             r'(?P<int>\S+)')
    result_list = [['switch','mac','ip','vlan','interface']]
    for file in filenames:
        hostname_match = hostname.search(file)
        with open(file) as file_obj:
            tmp_list = file_obj.readlines()
        for line in tmp_list:
            data_match = data_record.search(line)
            if data_match:
                result_list.append([f'''{hostname_match.group('host')}''',f'''{data_match.group('mac')}''',f'''{data_match.group('ip')}''',f'''{data_match.group('vlan')}''',f'''{data_match.group('int')}'''])
    with open(output, 'w') as file_obj:
        csv_writer_obj = csv.writer(file_obj)
        for elem in result_list:
            csv_writer_obj.writerow(elem)


if __name__ == '__main__':
    write_dhcp_snooping_to_csv(filenames, 'output_1.csv')