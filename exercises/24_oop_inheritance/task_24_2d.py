# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_command(self, cmd, **kwargs):
        result = super().send_command(cmd, **kwargs)
        self._check_error_in_command(cmd, result)
        return(result)

    def send_config_set(self, cfg_commands, ignore_errors=False):
        if ignore_errors:
            result = super().send_config_set(cfg_commands)
            return(result)
        else:
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
