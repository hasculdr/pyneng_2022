# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
from concurrent.futures import ThreadPoolExecutor
import yaml

from netmiko import ConnectHandler

def send_show_cmd(device, cmd):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        prompt = ssh.find_prompt()
        result = ssh.send_command(cmd)
    return(prompt + cmd + '\n' + result)

def devices_list(devices_file):
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    return(devices)

def send_show_command_to_devices(devices, command, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_obj_list = list()
        for dev in devices:
            future_obj = executor.submit(send_show_cmd, dev, command)
            future_obj_list.append(future_obj)
    with open(filename, 'w') as f:
        for obj in future_obj_list:
            f.write(obj.result())

if __name__ == "__main__":
    command = 'sh ip int br'
    devices_file = 'devices.yaml'
    filename = '19_2_result.txt'
    send_show_command_to_devices(devices_list(devices_file), command, filename)