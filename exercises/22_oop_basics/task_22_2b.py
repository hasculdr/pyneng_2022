# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
from textfsm import clitable

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.connection = telnetlib.Telnet(ip, port=23, timeout=10)
        self._write_line(username)
        self._write_line(password)
        self._write_line('enable')
        self._write_line(secret)
        self.connection.read_until(b'#', timeout=3)


    def _write_line(self, str):
        line = str.encode("ascii") + b"\n"
        return(self.connection.write(line))


    def send_show_command(self, show_command, parse=True, templates='templates', index='index'):
        if parse:
            attributes = {'Command': show_command, 'Vendor': 'cisco_ios'}
            self._write_line(show_command)
            output = self.connection.read_until(b'#', timeout=3).decode("utf-8")
            result = list()
            cli_table_obj = clitable.CliTable(index, templates)
            cli_table_obj.ParseCmd(output, attributes)
            header = list(cli_table_obj.header)
            length = len(header)
            for elem in cli_table_obj:
                temp_dict = dict.fromkeys(header)
                counter = 0
                while counter < length:
                    temp_dict[header[counter]] = elem[counter]
                    counter += 1
                result.append(temp_dict)
            return(result)
        else:
            self._write_line(show_command)
            return(self.connection.read_until(b'#', timeout=3).decode("utf-8"))
    

    def send_config_commands(self, config_commands):
        self._write_line('configure terminal')
        self.connection.read_until(b'#', timeout=3)
        if type(config_commands) == list:
            response = str()
            for cmd in config_commands:
                self._write_line(cmd)
                result = self.connection.read_until(b'#', timeout=3).decode("utf-8")
                response += result
        else:
            self._write_line(config_commands)
            response = self.connection.read_until(b'#', timeout=3).decode("utf-8")
        return(response)


print(CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco').send_config_commands(['interface fa0/1', 'no desc']))