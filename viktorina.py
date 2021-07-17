# Написать программу "Викторина": Выбрать минимум 5 известных людей и узнать дату их рождения. 
# Программа должна по очереди спрашивать у пользователя дату рождения знаменитости в формате ‘dd.mm.yyyy' 
# Например 03.01.2009, если пользователь ответил неверно, то выводим правильный ответ, но уже в следующем виде: 
# третье января 2009 года, склонением можно пренебречь 
# После того как пользователь ввел все ответы, программа считает и выводит на экран:
# - количество правильных ответов
# - количество ошибок
# - процент правильных ответов

import random
from datetime import date

def Game():
    game_data = {'А.С. Пушкин': date(1837,2,10), 'М.Ю. Лермонтов': date(1814,10,15), 'В.С. Высоцкий': date(1938,1,25),
                'Ю.А. Гагарин': date(1934,3,9), 'М.М. Жванецкий': date(1934,3,6)}
    num_questions = len(game_data)
    right_answers = 0

    resp = input('В игре "Викторина" Вам надо будет ответить верно на 5 вопросов. Сыграем (д/н)? >').lower ()
    if resp!='д':
        return

    while (len (game_data) > 0):
        choice = random.choice(list(game_data.items()))
        print (choice)
        resp = input('Вспомните, когда родился %s. Укажите дату как дд.мм.гггг >' %choice[0])
        print (resp)
        try:
            day,month,year = map(int, resp.split('.'))
            birthday = date(year, month, day)
        except:
            birthday = None
        
        if (birthday == None):
            resp = input("Хотите прервать игру (д/н)? >")
            if (resp.lower () == 'д'):
                print('Увидимся...')
                break
        else:
            game_data.pop(choice[0]) 
            if birthday == choice[1]:
                right_answers += 1
                print('Ответ верный !')
            else:
                print('Не угадали! Правильный ответ: %s родился %s ', choice[0], choice[1].strftime('%Y-%m-%d %H:%M'))

    print ('Ваш результат:')
    print (right_answers, ' - количество правильных ответов')
    print (num_questions - right_answers,  ' - количество ошибок')
    print (int((right_answers/num_questions)*100), ' - процент правильных ответов')

if __name__ == '__main__':
    Game()    