# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""


class IPAddress:
    def __init__(self, ippref):
        ip, mask = ippref.split('/')
        octets = ip.split('.')
        if len(octets) == 4:
            for elem in octets:
                if elem.isdigit():
                    if int(elem) not in range(256):
                        raise ValueError('Incorrect IPv4 address')
                else:
                    raise ValueError('Incorrect IPv4 address')
        else:
            raise ValueError('Incorrect IPv4 address')
        if mask.isdigit():
            if int(mask) not in range(8, 32):
                raise ValueError('Incorrect mask')
        else:
            raise ValueError('Incorrect mask')
        self.ippref = ippref
        self.ip = ip
        self.mask = int(mask)

    def __str__(self):
        return(f"IP address {self.ippref}")

    def __repr__(self):
        return(f"IPAddress('{self.ippref}')")
