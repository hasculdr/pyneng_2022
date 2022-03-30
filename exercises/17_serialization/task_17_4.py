# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.
В файле output первой строкой должны быть заголовки столбцов,
такие же как в файле source_log.

Для части пользователей запись только одна и тогда в итоговый файл надо записать
только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_str_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.
Вторая функция convert_datetime_to_str делает обратную операцию - превращает
объект datetime в строку.

Функции convert_str_to_datetime и convert_datetime_to_str использовать не обязательно.

"""

import datetime
import csv
from pprint import pprint



def convert_str_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")


def convert_datetime_to_str(datetime_obj):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M")

def write_last_log_to_csv(source_log, output):
    with open(source_log) as input_file:
        readed_data = csv.reader(input_file)
        csv_to_list = [elem for elem in readed_data]
        headers = csv_to_list.pop(0)
        result_dict = dict()
        for elem in csv_to_list:
            tmp_dict = dict()
            tmp_dict[elem[1]] = [(elem[0], elem[2])]
            if elem[1] not in result_dict:
                result_dict.update(tmp_dict)
            else:
                result_dict[elem[1]].append((elem[0], elem[2]))
    items_list = list(result_dict.items())
    result_list = list()
    result_list.append(headers)
    for thing in items_list:
            if len(thing[1]) == 1:
                result_list.append([thing[1][0][0], thing[0], thing[1][0][1]])
            else:
                data_comparing_list = list()
                for tupple_elem in thing[1]:
                    data_comparing_list.append(convert_str_to_datetime(tupple_elem[1]))
                    last_date_obj = max(data_comparing_list)
                    last_str_obj = convert_datetime_to_str(last_date_obj)
                for tupple_elem in thing[1]:
                    if last_str_obj in tupple_elem:
                        result_list.append([tupple_elem[0], thing[0], tupple_elem[1]])
    with open(output, 'w') as output_file:
        csv_writer_obj = csv.writer(output_file)
        for elem in result_list:
            csv_writer_obj.writerow(elem)
    #return(result_list)

if __name__ == '__main__':
    pprint(write_last_log_to_csv('mail_log.csv', 'new_log.csv'))