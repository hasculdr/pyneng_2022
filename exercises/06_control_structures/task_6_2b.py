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
while correct_ip is False:
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
        correct_ip = True
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