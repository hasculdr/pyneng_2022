# -*- coding: utf-8 -*-

import os
import sqlite3
import yaml
import glob
import re


def db_check():
    if os.path.exists('dhcp_snooping.db'):
        return True
    else:
        print('База данных не существует; перед добавлением данных ее нужно создать')
        return False

def switch_data_add():
    with open('switches.yml') as file_obj:
        # внутри будет словарь; ключ 'switches', значение - вложенный словарь
        data = yaml.safe_load(file_obj)
    values = list(data['switches'].items())
    print('Добавляю данные в таблицу switches...')
    for elem in values:
        with connection:
            try:
                connection.execute('INSERT into switches values (?, ?)', elem)
            except sqlite3.IntegrityError as err:
                print(f'При добавлении данных {elem} возникла ошибка: {err}')

def dhcp_data_add():
    files_list = glob.glob('new_data/sw*_dhcp_snooping.txt')
    regexp = re.compile(r'(?P<mac>(\S{2}:){5}\S{2})\s+'
                        r'(?P<ip>(\d+\.){3}\d+)'
                        r'\s+\d+\s+\S+\s+'
                        r'(?P<vlan>\d+)\s+'
                        r'(?P<intf>\S+)')
    actual_macs = set()
    macs_in_db = set()
    print('Добавляю данные в таблицу dhcp...')
    for filename in files_list:
        with open(filename) as f_obj:
            data = f_obj.readlines()
        for string in data:
            match = regexp.search(string)
            if match:
                data_dict = match.groupdict()
                switch_name = filename.rstrip('_dhcp_snooping.txt')
                data_dict['switch'] = switch_name
                data_dict['active'] = 1
                values = tuple(data_dict.values())
                actual_macs.add(data_dict['mac'])
                with connection:
                    connection.execute('INSERT OR REPLACE into dhcp values (?, ?, ?, ?, ?, ?)', values)
                    macs_in_db_cursor = connection.execute('SELECT mac FROM dhcp')
                    for elem in macs_in_db_cursor.fetchall():
                        macs_in_db.add(elem[0])
                    outdated_macs = macs_in_db - actual_macs
                    for elem in outdated_macs:
                        connection.execute(f"UPDATE dhcp SET active = 0 WHERE mac = '{elem}'")


if __name__ == '__main__':
    if db_check():
        connection = sqlite3.connect('dhcp_snooping.db')
        switch_data_add()
        dhcp_data_add()
        connection.close()