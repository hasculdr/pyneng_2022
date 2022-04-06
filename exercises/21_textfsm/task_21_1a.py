# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""
from textfsm import TextFSM

def parse_output_to_dict(template, command_output):
  result = list()
  with open(template) as template_obj:
    fsm_obj = TextFSM(template_obj)
    fsm_parse_result = fsm_obj.ParseText(command_output)
    headers = fsm_obj.header
    length = len(headers)
    for elem in fsm_parse_result:
      temp_dict = dict.fromkeys(headers)
      counter = 0
      while counter < length:
        temp_dict[headers[counter]] = elem[counter]
        counter += 1
      result.append(temp_dict)
  return(result)
if __name__ == "__main__":
  with open('output/sh_ip_int_br.txt') as output_obj:
    output = output_obj.read()
  print(parse_output_to_dict('templates/sh_ip_int_br.template', output))
