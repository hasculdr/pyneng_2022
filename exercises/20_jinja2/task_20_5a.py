# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
import yaml
import re

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    tuns_intf_str = list()
    ssh_src = ConnectHandler(**src_device_params)
    ssh_src.enable()
    output_src = ssh_src.send_command('show interf desc | inc Tu')
    intf_list_src = output_src.split('\n')
    for str in intf_list_src:
        match = re.search(r'Tu(\d+)', str)
        if match:
            tuns_intf_str.append(match.group(1)) # список с номерами tun-интерфейсов, тип элементов - строка
    ssh_dst = ConnectHandler(**dst_device_params)
    ssh_dst.enable()
    output_dst = ssh_dst.send_command('show interf desc | inc Tu')
    intf_list_dst = output_dst.split('\n')
    for str in intf_list_dst:
        match = re.search(r'Tu(\d+)', str)
        if match:
            tuns_intf_str.append(match.group(1)) # список с номерами tun-интерфейсов, тип элементов - строка
    if len(tuns_intf_str) == 0:
        vpn_data_dict['tun_num'] = '0'
    else:
        dedup = set(tuns_intf_str) # множество уберет продублированные интерфейсы
        tuns_intf_int = list()
        sorted_tuns_intf_int = list()
        for num in dedup:
            tuns_intf_int.append(int(num)) # конвертируем все номера в числа
            sorted_tuns_intf_int = sorted(tuns_intf_int)
        for num in sorted_tuns_intf_int:
            index = sorted_tuns_intf_int.index(num)
            last_elem = sorted_tuns_intf_int[-1]
            if index != sorted_tuns_intf_int.index(last_elem):
                if num + 1 == sorted_tuns_intf_int[index + 1]:
                    pass
                else:
                    vpn_data_dict['tun_num'] = f'{num + 1}'
                    break
            else:
                vpn_data_dict['tun_num'] = f'{num + 1}'
    env = Environment(
        loader=FileSystemLoader('.'),
        trim_blocks=True,
        lstrip_blocks=True)
    templ_src = env.get_template(src_template)
    templ_dst = env.get_template(dst_template)
    set_commands_src_str = templ_src.render(vpn_data_dict)
    set_commands_dst_str = templ_dst.render(vpn_data_dict)
    set_commands_src = set_commands_src_str.split('\n')
    set_commands_dst = set_commands_dst_str.split('\n')
    configure_src = ssh_src.send_config_set(set_commands_src)
    configure_dst = ssh_dst.send_config_set(set_commands_dst)
    ssh_src.disconnect()
    ssh_dst.disconnect()
    return(configure_src, configure_dst,)

if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    src_template = 'templates/gre_ipsec_vpn_1.txt'
    dst_template = 'templates/gre_ipsec_vpn_2.txt'
    print(configure_vpn(devices[0], devices[1], src_template, dst_template, data))