# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений
  и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы (именно в этом порядке):
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается
на sh_vers. Вы можете раскомментировать строку print(sh_version_files),
чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import re
import csv
from pprint import pprint

sh_version_files = glob.glob("sh_vers*")
#print(sh_version_files)

headers = ["hostname", "ios", "image", "uptime"]

def parse_sh_version(string):
  ios_reg = re.compile(r'Cisco IOS Software,.+?, Version (.+?),')
  image_reg = re.compile(r'System image file is "(.+)"')
  uptime_reg = re.compile(r'uptime is (.+)')
  ios = ios_reg.search(string)
  image = image_reg.search(string)
  uptime = uptime_reg.search(string)
  return((ios.group(1), image.group(1), uptime.group(1),))

def write_inventory_to_csv(data_filenames, csv_filename):
  result = list()
  hostname_reg = re.compile(r'.+_(.+)\.')
  for elem in data_filenames:
    with open(elem) as file:
      string = file.read()
      data = list(parse_sh_version(string))
      hostname = hostname_reg.search(elem)
      data.insert(0, hostname.group(1))
      result.append(data)
  result.insert(0, headers)
  with open(csv_filename, 'w') as file:
    csv_writer_obj = csv.writer(file)
    for elem in result:
      csv_writer_obj.writerow(elem)

if __name__ == '__main__':
  (write_inventory_to_csv(sh_version_files, 'output_2.csv'))