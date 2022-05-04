# -*- coding: utf-8 -*-

import os
import sqlite3


if os.path.exists('dhcp_snooping.db'):
    print('База данных уже существует')
else:
    print('Создаю базу данных...')
    with open('dhcp_snooping_schema.sql') as f_obj:
        schema_create = f_obj.read()
    connection = sqlite3.connect('dhcp_snooping.db')
    connection.executescript(schema_create)
    print('Готово')
