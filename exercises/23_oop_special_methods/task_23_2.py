# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка

Тест проверяет подключение с параметрами из файла devices.yaml. Там должны быть
указаны доступные устройства.
"""
import telnetlib


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.connection = telnetlib.Telnet(ip, port=23)
        self._write_line(username)
        self._write_line(password)
        self._write_line('enable')
        self._write_line(secret)
        self.connection.read_until(b'#', timeout=3)

    def __enter__(self):
        return(self)

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def _write_line(self, str):
        line = str.encode("ascii") + b"\n"
        return(self.connection.write(line))

    def send_show_command(self, show_command):
        self._write_line(show_command)
        return(self.connection.read_until(b'#', timeout=3).decode("ascii"))


with CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco') as telnet_connection:
    print(telnet_connection.send_show_command('show clock'))
