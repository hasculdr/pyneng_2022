# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
userinput = input('Введите ip-адрес в формате "10.0.1.1": ')

octet_list = userinput.split('.')
try:
   if len(octet_list) == 4:
      for elem in octet_list:
         if int(elem) in range(0,256):
            pass
         else:
            raise
   else:
      raise
   if int(octet_list[0]) in range(1,224):
      print('unicast')
   elif int(octet_list[0]) in range(224,240):
      print('multicast')
   elif userinput == '255.255.255.255':
      print('local broadcast')
   elif userinput == '0.0.0.0':
      print('unassigned')
   else:
      print('unused')
except:
   print('Неправильный IP-адрес')