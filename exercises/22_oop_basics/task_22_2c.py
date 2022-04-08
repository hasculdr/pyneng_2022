# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""
import telnetlib
from textfsm import clitable
import re

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.connection = telnetlib.Telnet(ip, port=23, timeout=10)
        self.ip = ip
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


    def send_config_commands(self, config_commands, strict=True):
        self._write_line('configure terminal')
        self.connection.read_until(b'#', timeout=3)
        err_template = re.compile(r'%\s(.+)?\n')
        if strict:
            if type(config_commands) == list:
                response = str()
                for cmd in config_commands:
                    self._write_line(cmd)
                    result = self.connection.read_until(b'#', timeout=3).decode("utf-8")
                    if '%' in result:
                        err_msg = err_template.search(result).group(1)
                        raise ValueError(f'''При выполнении команды "{cmd}" на устройстве {self.ip} возникла ошибка -> {err_msg}''')
                    else:
                        response += result
            else:
                self._write_line(config_commands)
                response = self.connection.read_until(b'#', timeout=3).decode("utf-8")
                if '%' in response:
                    err_msg = err_template.search(response).group(1)
                    raise ValueError(f'''При выполнении команды "{config_commands}" на устройстве {self.ip} возникла ошибка -> {err_msg}''')
            return(response)
        else: # strict=False
            if type(config_commands) == list:
                response = str()
                for cmd in config_commands:
                    self._write_line(cmd)
                    result = self.connection.read_until(b'#', timeout=3).decode("utf-8")
                    if '%' in result:
                        err_msg = err_template.search(result).group(1)
                        print(f'''При выполнении команды "{cmd}" на устройстве {self.ip} возникла ошибка -> {err_msg}''')
                        response += result
                    else:
                        response += result
            else:
                self._write_line(config_commands)
                response = self.connection.read_until(b'#', timeout=3).decode("utf-8")
                if '%' in response:
                    err_msg = err_template.search(response).group(1)
                    print(f'''При выполнении команды "{config_commands}" на устройстве {self.ip} возникла ошибка -> {err_msg}''')
            return(response)


print(CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco').send_config_commands(["interface loop55", "ip address 5.5.5.5 255.255.255.255"], strict=True))