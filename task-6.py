'''
Реализовать программу, при помощи которой двое пользователей могут
играть в «Клондайк». Правила игры следующие. Игра ведётся на
игровом поле размером 10 на 10 клеток. Игроки по очереди выставляют в
любую свободную клетку по отметке, и тот игрок, после чьего хода
получилась цепочка длиной хотя бы в три отметки, проигрывает. При этом в
цепочке считаются как свои отметки, так и отметки соперника, у игровых
фишек как бы нет хозяина. Цепочка — это ряд фишек, следующая фишка в
котором примыкает к предыдущей с любого из восьми направлений.
Взаимодействие с программой производится через консоль. Игровое поле
изображается в виде десяти текстовых строк и перерисовывается при
каждом изменении состояния поля. При запросе данных от пользователя
программа сообщает, что ожидает от пользователя (например, координаты
очередного хода) и проверяет корректность ввода. Программа должна
уметь автоматически определять окончание партии и ее победителя. Сама
программа НЕ ходит, т.е. не пытается ставить в клетки отметки с целью
выиграть игру.
'''

import random

player_one = input('Write your nickname:\n') #Запрашивает никнеймы двух игроков
player_two = input('Write your nickname:\n')
player = 1 #Устанавливает счетчик ходов (player = 1)

#Создает игровое поле 10x10, заполненное символами '*'
no_hit = '*' #no_hit = '*' - пустая клетка
hit = 'X' #hit = 'X' - занятая клетка
game_board = []
for width in range (10):
    game_board_mini = []
    for hight in range (10):
        game_board_mini.append(no_hit)
    game_board.append(game_board_mini)

#Случайным образом выбирает, кто ходит первым
coin_flip = [player_one, player_two]
rng = random.choice(coin_flip)
print(rng, '- you start, you are player 1\n')

#Выводит начальное игровое поле
print('Playing board:')
print(*game_board, sep='\n')


def end(game_board): #Функция проверки окончания игры
    line_3 = 0
    for line in range (0,8): #Проверяет, есть ли на поле цепочка из 3 отметок подряд
        for row in range (0,8):
            if game_board[line][row] == hit == game_board[line][row+1] == game_board[line][row+2] or game_board[line][row] == hit == game_board[line+1][row] == game_board[line+2][row] or game_board[line][row] == hit == game_board[line+1][row+1] == game_board[line+2][row+2]:
                line_3 = 1
    for line in range (0,10):
        for row in range (0,8):
            if game_board[line][row] == hit == game_board[line][row+1] == game_board[line][row+2]:
                line_3 = 1
    for line in range (0,8):
        for row in range (0,10):
            if game_board[line+1][row] == hit == game_board[line+2][row] == game_board[line][row]:
                line_3 = 1
    return line_3
    #Возвращает 1 если игра окончена, 0 если продолжается

def line_check(): #Рекурсивно запрашивает номер строки, пока не получит корректное число
    try:
        line = int(input('Chose the line: '))
        return line
    except ValueError:
        print('Write in numbers please')
        return line_check()
    
def row_check(): #Аналогично запрашивает номер столбца
    try:
        row = int(input('Now the row: '))
        return row
    except ValueError:
        print('Write in numbers please')
        return row_check()


while not end(game_board): #Основной игровой цикл
    my_line = line_check() #Игроки по очереди делают ходы
    my_row = row_check()
    if 0 <= my_row < 10 and 0 <= my_line < 10: #Проверяет корректность координат и что клетка свободна
        if game_board[my_line][my_row] != hit:
            game_board[my_line][my_row] = hit
    print('Playing board:')
    print(*game_board, sep='\n') #Обновляет и отображает игровое поле
    player+=1
else: #Объявляет победителя когда игра заканчивается
    print('You Died')
    if player%2 == 0: print('player 1 - you win')
    if player%2 != 0: print('player 2 - you win')