# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
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
                switch_name = filename.rstrip('_dhcp_snooping.txt').lstrip('new_data/')
                data_dict['switch'] = switch_name
                data_dict['active'] = 1
                values = tuple(data_dict.values())
                actual_macs.add(data_dict['mac'])
                with connection:
                    connection.execute('INSERT OR REPLACE into dhcp values (?, ?, ?, ?, ?, ?, datetime(\'now\'))', values)
                    macs_in_db_cursor = connection.execute('SELECT mac FROM dhcp')
                    for elem in macs_in_db_cursor.fetchall():
                        macs_in_db.add(elem[0])
                    outdated_macs = macs_in_db - actual_macs
                    for elem in outdated_macs:
                        connection.execute(f"UPDATE dhcp SET active = 0 WHERE mac = '{elem}'")

def dhcp_old_data_remove():
    current_date = datetime.now()
    old_data_cursor = connection.execute('SELECT mac, last_active from dhcp WHERE active = 0')
    old_data = old_data_cursor.fetchall()
    tmp = [(elem[0], datetime.fromisoformat(elem[1])) for elem in old_data]
    for value in tmp:
        if current_date - value[1] > timedelta(days=7):
            with connection:
                connection.execute(f"DELETE from dhcp WHERE mac = '{value[0]}'")


if __name__ == '__main__':
    if db_check():
        connection = sqlite3.connect('dhcp_snooping.db')
        switch_data_add()
        dhcp_data_add()
        dhcp_old_data_remove()
        connection.close()