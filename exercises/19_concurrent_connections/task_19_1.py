# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
from concurrent.futures import ThreadPoolExecutor
import logging
import subprocess

from datetime import datetime

limit = 4
ip_list = ['192.168.100.1', '192.168.100.2', '192.168.100.3', '192.168.100.4']

def ping_single_ip(addr):
    logging.info(f'''===> {datetime.now().time()} Trying: {addr}''')
    result = subprocess.run(['ping', '-c', '3', '-n', addr], stdout=subprocess.PIPE, encoding='utf-8')
    logging.info(f'''<=== {datetime.now().time()} Done: {addr}''')
    if result.returncode == 0:
        return(True)
    else:
        return(False)

def ping_ip_addresses(ip_list, limit=3):
    alive = list()
    unreachable = list()
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_obj_list = list()
        for addr in ip_list:
            future_obj = executor.submit(ping_single_ip, addr)
            future_obj_list.append(future_obj)
        for ip, f_obj in zip(ip_list,future_obj_list):
            status = f_obj.result()
            if status:
                alive.append(ip)
            else:
                unreachable.append(ip)
    return((alive, unreachable))

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

if __name__ == "__main__":
    print(ping_ip_addresses(ip_list, limit))