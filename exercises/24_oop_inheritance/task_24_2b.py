# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
from netmiko.cisco.cisco_ios import CiscoIosSSH


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.ip = device_params['host']
        self.enable()

    def _check_error_in_command(self, cmd, cmd_result):
        if '%' in cmd_result:
            start = cmd_result.find('%')
            raise ErrorInCommand(f"При выполнении команды \"{cmd}\" на устройстве {self.ip} возникла ошибка \"{cmd_result[start:-1]}\"")

    def send_command(self, cmd):
        result = super().send_command(cmd)
        self._check_error_in_command(cmd, result)
        return(result)

    def send_config_set(self, cfg_commands):
        if type(cfg_commands) == list:
            result = str()
            for cmd in cfg_commands:
                tmp = super().send_config_set(cmd)
                self._check_error_in_command(cmd, tmp)
                result += tmp
            return(result)
        else:
            result = super().send_config_set(cfg_commands)
            self._check_error_in_command(cfg_commands, result)
            return(result)

class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


device_params = {
    "device_type": "cisco_ios",
    "host": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

