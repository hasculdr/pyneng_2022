# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
correct_ip = False
first_octet = str()
while correct_ip == False:
    userinput = input('Введите ip-адрес в формате "10.0.1.1": ')
    octet_list = userinput.split('.')
    if len(octet_list) == 4:
        first, second, third, fourth = octet_list
        if first.isdigit() and second.isdigit() and third.isdigit() and fourth.isdigit():
            if int(first) in range(0,256) and int(second) in range(0,256) and int(third) in range(0,256) and int(fourth) in range(0,256):
                correct_ip = True
                if int(first) in range(1,224):
                    print('unicast')
                elif int(first) in range(224,240):
                    print('multicast')
                elif userinput == '255.255.255.255':
                    print('local broadcast')
                elif userinput == '0.0.0.0':
                    print('unassigned')
                else:
                    print('unused')
            else:
                print('Неправильный IP-адрес')
        else:
            print('Неправильный IP-адрес')
    else:
            print('Неправильный IP-адрес')
