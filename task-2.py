'''
КРЕСТИКИ-НОЛИКИ
'''
'''
Реализовать программу, при помощи которой двое пользователей могут играть в
«Крестики-нолики» на поле 3 на 3. Взаимодействие с программой производится через
консоль. Игровое поле изображается в виде трех текстовых строк и перерисовывается при
каждом изменении состояния поля. При запросе данных от пользователя программа
сообщает, что ожидает от пользователя (в частности, координаты новой отметки на поле)
и проверяет корректность ввода. Программа должна уметь автоматически определять, что
партия окончена, и сообщать о победе одного из игроков или о ничьей. Сама программа
НЕ ходит, т.е. не пытается ставить крестики и нолики с целью заполнить линию.
'''

print('''Это игра крестики-нолики. Первый игрок играет за крестики,
a второй за нолики.''')
line1 = [[' '], [' '], [' ']]
line2 = [[' '], [' '], [' ']]
line3 = [[' '], [' '], [' ']]
line_list = [line1, line2, line3] 
print(line1)
print(line2)
print(line3)


def win_first(line1, line2, line3):
    """Функция перебирает все варианты победы первого игрока"""
    flag = 0
    if (line1 == [['×'], ['×'], ['×']] or line2 == [['×'], ['×'], ['×']] or
        line3 == [['×'], ['×'], ['×']] or
        (line1[0] == line2[0] == line3[0] == ['×']) or 
        (line1[1] == line2[1] == line3[1] == ['×']) or
        (line1[2] == line2[2] == line3[2] == ['×']) or
        (line1[0] == line2[1] == line3[2] == ['×']) or
        (line1[2] == line2[1] == line3[0] == ['×'])):
        flag = 1
    return flag


def win_second(line1, line2, line3):
    """Функция перебирает все варианты победы второго игрока"""
    flag = 0
    if (line1 == [['0'], ['0'],['0']] or line2 == [['0'], ['0'], ['0']] or
            line3 == [['0'], ['0'], ['0']] or
        (line1[0] == line2[0] == line3[0] == ['0']) or
            (line1[1] == line2[1] == line3[1] == ['0']) or
        (line1[2] == line2[2] == line3[2] == ['0']) or
        (line1[0] == line2[1] == line3[2] == ['0']) or
            (line1[2] == line2[1] == line3[0] == ['0'])) == 1:
        flag = 1
    return flag


def end(line1, line2, line3):
    """Функция перебирает все варианты окончания партии"""
    flag = 0
    if (line1[0] == line2[0] == line3[0] != [' '] or 
        line1[1] == line2[1] == line3[1] != [' '] or 
        line1[2] == line2[2] == line3[2] != [' '] or 
        line1[0] == line1[1] == line1[2] != [' '] or 
        line2[0] == line2[1] == line2[2] != [' '] or 
        line3[0] == line3[1] == line3[2] != [' '] or 
        line1[0] == line2[1] == line3[2] != [' '] or 
        line1[2] == line2[1] == line3[0] != [' '] or
        line1.count([' ']) + line2.count([' ']) + line3.count([' ']) == 0):
        flag = 1
    return flag    
   
count = 0 

while end(line1, line2, line3) != 1:
    if count % 2 == 0:
        player = 'Первый игрок'
    else:
        player = 'Второй игрок'
    argument = 0
    while argument != 1: #выполняется пока игра не окончена.
        arg_move = 0 
        while arg_move != 1:
            move_line = input(f"{player}, введите номер строки, на" + '\n' +
                              'которой хотите поставить знак '
                               '(целое число от 1 до 3): \n')
            move_column = input(f"{player}, введите номер столбца, на" + '\n' +
                              'котором хотите поставить знак '
                               '(целое число от 1 до 3): \n')
            if (move_line in ['1', '2', '3'] and move_column in
                ['1', '2', '3']):
                arg_move = 1 
                move_line = int(move_line) 
                move_column = int(move_column) 
            else:
                print('Ошибка, введите целое число от 1 до 3 вкл \n')
        if count % 2 == 0: 
            if line_list[move_line-1][move_column-1] == [' ']:
                line_list[move_line-1][move_column-1] = ['×']
                argument = 1
                count += 1
            else:
                print('На этой клетке уже стоит знак, поставьте знак '
                      'на пустую клетку \n')
        else:
            if line_list[move_line-1][move_column-1] == [' ']:
                line_list[move_line-1][move_column-1] = ['0']
                argument = 1
                count += 1 
            else:
                print('На этой клетке уже стоит знак, поставьте знак '
                      'на пустую клетку \n')
    print(line1)
    print(line2)
    print(line3)

if win_first(line1, line2, line3):
    print('Победил первый игрок')
elif win_second(line1, line2, line3):
    print('Победил второй игрок')
else:
    print('Ничья')


input("Нажмите Enter для выхода!")