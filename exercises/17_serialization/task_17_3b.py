# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий
для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно,
чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии,
но и удалять "дублирующиеся" соединения (их лучше всего видно на схеме, которую
генерирует функция draw_topology из файла draw_network_graph.py).
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Из-за того что один и тот же линк описывается дважды, на схеме будут лишние соединения.
Задача оставить только один из этих линков в итоговом словаре, не важно какой.

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии
с помощью функции draw_topology.
Не копировать код функции draw_topology из файла draw_network_graph.py.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть "дублирующихся" линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
from draw_network_graph import draw_topology
import yaml
from pprint import pprint

def transform_topology(yaml_file):
    with open(yaml_file) as input:
        redundant_dict = yaml.safe_load(input)
    redundant_dict_with_tuples = dict()
    for thing in redundant_dict: # thing - ключ трехуровневого словаря, значение - двухуровневый словарь
        local_device = thing # это возвращает ключ верхрего уровня
        for another_thing in redundant_dict[thing]: # another_thing - ключ двухуровневого словаря, соответствующее значение - словарь
            for elem in redundant_dict[thing][another_thing]: # elem - ключ нижнего слованя, соответствующее значение - строка
                remote_port = redundant_dict[thing][another_thing][elem] # значение нижнего словаря
                remote_device = elem # ключ нижнего словаря
                local_port = another_thing # ключ "среднего словаря"
                temp = {(local_device, local_port): (remote_device, remote_port)}
                redundant_dict_with_tuples.update(temp)
    tmp_list = list(redundant_dict_with_tuples.items())
    for elem_big in tmp_list:
        for elem_small in tmp_list:
            if elem_big[0] == elem_small[1]:
                tmp_list.remove(elem_big)
    normalized_dict = dict(tmp_list)
    return(normalized_dict)

if __name__ == '__main__':
    result = transform_topology('topology.yaml')
    pprint(transform_topology('topology.yaml'))
    draw_topology(result, "img/my_topology")