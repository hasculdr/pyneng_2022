# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from sys import argv

filein = argv[1]
fileout = argv[2]
ignore.append('!')
first, second, third, fourth = ignore
with open(filein) as filein_obj, open(fileout, 'w') as fileout_obj:
    for line in filein_obj:
        if first not in line and second not in line and third not in line and fourth not in line:
            fileout_obj.write(line)
        else:
            pass