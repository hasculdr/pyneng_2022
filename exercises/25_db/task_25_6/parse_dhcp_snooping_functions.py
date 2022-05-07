# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import os
import sqlite3
import yaml
import glob
import re
from tabulate import tabulate

def create_db(name, schema):
    if os.path.exists(name):
        print('База данных уже существует')
    else:
        with open(schema) as f_obj:
            schema_create = f_obj.read()
        connection = sqlite3.connect(name)
        connection.executescript(schema_create)
        print('Готово')

def db_check(db_file):
    if os.path.exists(db_file):
        return True
    else:
        print('База данных не существует; перед добавлением данных ее нужно создать')
        return False

def switch_data_add(db_file, filename):
    for elem in filename:
        with open(elem) as file_obj:
            # внутри будет словарь; ключ 'switches', значение - вложенный словарь
            data = yaml.safe_load(file_obj)
        values = list(data['switches'].items())
        connection = sqlite3.connect(db_file)
        for elem in values:
            with connection:
                try:
                    connection.execute('INSERT into switches values (?, ?)', elem)
                except sqlite3.IntegrityError as err:
                    print(f'При добавлении данных {elem} возникла ошибка: {err}')
        connection.close()

def dhcp_add_data(db_file, filename):
    files_list = glob.glob('sw[0-9]_dhcp_snooping.txt')
    regexp = re.compile(r'(?P<mac>(\S{2}:){5}\S{2})\s+'
                        r'(?P<ip>(\d+\.){3}\d+)'
                        r'\s+\d+\s+\S+\s+'
                        r'(?P<vlan>\d+)\s+'
                        r'(?P<intf>\S+)')
    actual_macs = set()
    macs_in_db = set()
    connection = sqlite3.connect(db_file)
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
    connection.close()

def dhcp_old_data_remove(db_file):
    current_date = datetime.now()
    connection = sqlite3.connect(db_file)
    old_data_cursor = connection.execute('SELECT mac, last_active from dhcp WHERE active = 0')
    old_data = old_data_cursor.fetchall()
    tmp = [(elem[0], datetime.fromisoformat(elem[1])) for elem in old_data]
    for value in tmp:
        if current_date - value[1] > timedelta(days=7):
            with connection:
                connection.execute(f"DELETE from dhcp WHERE mac = '{value[0]}'")
    connection.close()

def add_data_switches(db_file, filename):
    if db_check(db_file):
        switch_data_add(db_file, filename)

def add_data(db_file, filename):
    if db_check(db_file):
        dhcp_add_data(db_file, filename)
        dhcp_old_data_remove(db_file)

def get_data(db_file, key, value):
    act_header = 'Активные записи:'
    inact_header = 'Неактивные записи:'
    act_query = f"SELECT * from dhcp WHERE {key} = '{value}' AND active = 1"
    inact_query = f"SELECT * from dhcp WHERE {key} = '{value}' AND active = 0"
    connection = sqlite3.connect(db_file)
    act_data = connection.execute(act_query)
    inact_data = connection.execute(inact_query)
    act_result = tabulate(act_data)
    inact_result = tabulate(inact_data)
    connection.close()
    if len(act_result) > 0 and len(inact_result) > 0:
        print(act_header, act_result, inact_header, inact_result, sep='\n\n')
    elif len(act_result) > 0 and len(inact_result) == 0:
        print(act_header, act_result, sep='\n\n')
    elif len(act_result) == 0 and len(inact_result) > 0:
        print(inact_header, inact_result, sep='\n\n')
    else:
        print('В таблице dhcp нет записей')

def get_all_data(db_file):
    act_header = 'Активные записи:'
    inact_header = 'Неактивные записи:'
    connection = sqlite3.connect(db_file)
    act_data = connection.execute('SELECT * from dhcp WHERE active = 1')
    inact_data = connection.execute('SELECT * from dhcp WHERE active = 0')
    act_result = tabulate(act_data)
    inact_result = tabulate(inact_data)
    print(act_header, act_result, inact_header, inact_result, sep='\n\n')
    connection.close()