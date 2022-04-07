# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


"""
from pprint import pprint
class Topology:
    def __init__(self, topology_example):
        self.topology = self._normalize(topology_example)
    def _normalize(self, topology_example):
        tmp_list = list(topology_example.items())
        for elem_big in tmp_list:
            for elem_small in tmp_list:
                if elem_big[0] == elem_small[1]:
                    tmp_list.remove(elem_big)
        return(dict(tmp_list))
    def delete_link(self, key, value):
        if self.topology.get(key):
            del self.topology[key]
        elif self.topology.get(value):
            del self.topology[value]
        else:
            print("Такого соединения нет")
    def delete_node(self, node):
        delete_this = list()
        for key in self.topology:
            if node in key:
                delete_this.append(key)
            elif node in self.topology[key]:
                delete_this.append(key)
        if len(delete_this) > 0:
            for elem in delete_this:
                del self.topology[elem]
        else:
            print("Такого устройства нет")
    def add_link(self, key, value):
        link_check = False
        port_check = False
        for elem in self.topology:
            example = (elem, self.topology[elem],)
            if example == (key, value,):
                print('Такое соединение существует')
                link_check = True
                break
            elif elem == key and self.topology[elem] != value:
                print('Cоединение с одним из портов существует')
                port_check = True
                break
            else:
                pass
        if not link_check and not port_check:
            self.topology[key] = value

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}