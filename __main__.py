from ugadai import *
import viktorina as VIK
from LichnyiSchet import PersonalAccount 

if __name__ == '__main__':
    
    while (1):
        print('Вы в главном меню\n\n\
        (1) Личный кабинет\
        (2) Игра "Викторина"\
        (3) Игра "Загадай число"\
        (0) Выход')

        resp = input('Укажите нужный пункт >').strip()
        if resp=='0':
            print ('Что наша жизнь? Игра!')
            break
        elif resp=='1':
            PersonalAccount()
        elif resp=='2':
            VIK.Game()
        elif resp=='3':
            Game()
