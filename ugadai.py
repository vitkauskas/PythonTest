# Написать программу “Угадай число”. Программа должна с помощью наводящих вопросов отгадать число.
import random

def Game():
    game_range = set(range(1, 11))
    answers = set()

    print('Пожалуйста, задумайте число от 1 до 10, а я его попробую угадать.')

    resp = input("Готовы (д/н)? >").lower ()
    if resp!='д':
        return

    while (True):
        if len (game_range) == 0:
            print ('Вы сжульничали!!!')
            break

        num = random.choice(list(game_range))
        resp = input('%d - это верный ответ (д/н)? >' %num)

        if (resp == 'н'):
            game_range.remove(num) 
            print('Дайте еще подумать...')
        elif (resp.lower () == 'д'):
            print('Это моя маленькая победа!')
            break
        else:
            resp = input('Хотите прервать игру (д/н)? >')
            if (resp.lower () == 'д'):
                print('Увидимся...')
                break

if __name__ == '__main__':
    Game()
