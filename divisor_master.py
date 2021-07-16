# ************************************************** LIGHT ***************************************
# Необходимо реализовать модуль divisor_master. Все функции модуля принимают на
# вход натуральные числа от 1 до 1000. Модуль содержит функции:
# 1. проверка числа на простоту (простые числа - это те числа у которых делители
# единица и они сами);
# 2. выводит список всех делителей числа;
# 3. выводит самый большой простой делитель числа.

def func_ПроверкаНаПростоеЧисло(num):
    if (num<=1):
        return False
    elif (num==2):    
        return True
    else:
        for d in range (2, int(num ** 0.5) + 1):
            if (num%d == 0):
                return False
        return True

def func_СписокВсехДелителейЧисла(num):
    result = []
    for d in range (1, num+1):
        if (num%d == 0):
            result += [d]
    return result

from itertools import chain

# вариант с lambda
l_СписокВсехДелителейЧисла = lambda num: sorted(list(chain(*((d, num // d) for d in range(1, int(num ** 0.5) + 1) if num % d == 0))))

def func_СписокПростыхДелителейЧисла(num):
    if num < 1: 
        return None
    result = []
    
    for i in range (1, num+1):
        if (num % i == 0):
            # проверяем, что i простое
            i_is_prime = True
            for j in range (2, int(i ** 0.5) + 1):
                if (i%j == 0):
                    i_is_prime = False
                    break # выходим, если находим делитель
            if (i_is_prime): # Если делителей не было найдено, добавляем
                result += [i]
    
    return result

def func_НаибольшийПростойДелительЧисла(num):
    if num < 1: 
        return None
    for i in range (num, 1, -1):
        if (num % i == 0):
            # проверяем, что i простое
            i_is_prime = True
            for j in range (2, int(i ** 0.5) + 1):
                if (i%j == 0):
                    i_is_prime = False
                    break # выходим, если находим делитель
            if (i_is_prime): # Если делителей числа не было найдено, то возвращаем найденное число
                return i
    return None

# ************************************************** PRO ***************************************
# 2. функция выводит каноническое разложение числа на простые множители
# https://zaochnik.com/spravochnik/matematika/delimost/razlozhenie-chisel-na-prostye-mnozhiteli/
# 3. функция выводит самый большой делитель (не обязательно простой) числа

def funcРазложениеЧислаНаПростыеМножители(num):
    primes = [2] # составим список простых чисел

    result = []
    while (num>1):
        # Перебираем простые числа
        for d in primes:
            # print ('>', d)
            if (num%d == 0):
                result += [d]
                num = num // d
                # print ('нашли множитель', d)
                break
            if primes[len(primes)-1] == d:
                # добавим новое простое число 
                for i in range (d+1, int(num**0.5)+1): 
                    if func_ПроверкаНаПростоеЧисло (i):
                        primes += [i]
                        # print ('новое простое число', i)
                        if num%i==0:
                            break
                # если не нашли новый делитель - простое число, 
                # то считаем num - простым числом 
                if num%i != 0:
                    # print (num, 'есть простое число')
                    result += [num]
                    num = 1
                    break

    result = sorted(result) # каноническое разложение
    return result

def func_НаибольшийДелительЧисла(num):
# Само число и 1 исключаем из результата
    if num <= 2:
        return None
    for i in range (num-1, 1, -1):
        if (num % i == 0):
            return i
