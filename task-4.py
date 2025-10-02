'''
Реализовать программу, с которой можно играть в игру «19».
Правила игры следующие. Нужно выписать подряд числа от 1 до 19: в
строчку до 9, а потом начать следующую строку, в каждой клетке по 1
цифре. Затем игроку необходимо
вычеркнуть парные цифры или дающие в сумме 10 Условие — пары
должны находиться рядом или через зачеркнутые цифры по горизонтали
или по вертикали. После того как все возможные пары вычеркнуты,
оставшиеся цифры переписываются в конец таблицы. Цель — полностью
вычеркнуть все цифры. Взаимодействие с программой производится через
консоль. Игровое поле изображается в виде трех текстовых строк и
перерисовывается при каждом изменении состояния поля. При запросе
данных от пользователя программа сообщает, что ожидает от
пользователя (в частности, координаты очередного хода) и проверяет
корректность ввода. Программа должна уметь автоматически определять, что 
нужно выписать новые строки с цифрами и то, что партия окончена.
Сама программа НЕ ходит, т.е. не пытается выбирать пары цифр с целью
окончить игру.
'''

def check(line1, column1, line2, column2):  #проверка правильности введения координат.
    if line1 == line2 and column1 == column2:  #проверка на совпадение координат
        return 0
    if gf[line1][column1] == '-' or gf[line2][column2] == '-':  # в ячейке не должно быть "-"
        return 0
    if gf[line1][column1] + gf[line2][column2] == 10:  # числа можно вычеркнуть ,если их сумма 10
        return 1
    if gf[line1][column1] == gf[line2][column2]:  # если числа  равны 
        if column1 == column2 or line1 == line2:  # если введены координаты с одной линии или с одного столбца 
            if abs(column1 - column2) == 1 or abs(line1 - line2) == 1:  # если введены координаты соседних ячеек 
                return 1
            else:
                if column1 == column2:  # если стоят в одном стобце 
                    if gf[1][column1] == '-':
                        return 1
                    else:
                        return 0
                if line1 == line2:
                    for c in range(min(column1, column2) + 1, max(column1, column2)):  # если стоят в одной линии 
                        if gf[line1][c] != '-':
                            return 0
                    return 1
        else:
            return 0


def finish(gf):  # проверка нахождение ячейки для взаимодействия 
    if gf.count('-') == 26:
        return 0
    else:
        for line1 in range(3):
            for column1 in range(9):
                for line2 in range(3):
                    for column2 in range(9):
                        if check(line1, column1, line2, column2) == 1:
                            return 1
        return 0


def finalgamefield(gf):  #  финальное игровое поле 
    lastslot = 0
    if gf.count('-') == 26 and gf[2][8] == '9':
        return gf
    for line1 in range(3):
        for column1 in range(9):
            if gf[2 - line1][8 - column1] != '-':
                gf[2 - (lastslot // 9)][8 - lastslot] = gf[2 - line1][8 - column1]
                gf[2 - line1][8 - column1] = '-'
                lastslot += 1
    return (gf)


gf = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 1, 1, 2, 1, 3, 1, 4, 1], [5, 1, 6, 1, 7, 1, 8, 1, 9]]

gameover = 0
while gameover == 0:
    if finish(gf) == 1:
        print('   1 2 3 4 5 6 7 8 9')
        print(' -------------------')
        print('1| ' + ''.join([str(x) + ' ' for x in gf[0]]))
        print('2| ' + ''.join([str(x) + ' ' for x in gf[1]]))
        print('3| ' + ''.join([str(x) + ' ' for x in gf[2]]))
        line1 = int(input('Номер линии первого числа: ')) - 1
        column1 = int(input('Номер столбца первого числа: ')) - 1
        line2 = int(input('Номер линии второго числа: ')) - 1
        column2 = int(input('Номер столбца второго числа: ')) - 1
        if check(line1, column1, line2, column2) == 1:
            gf[line1][column1], gf[line2][column2] = '-', '-'
        else:
            print('Неверные координаты')
    else:
        print('Игра окончена!')
        gameover = 1
        fgf = finalgamefield(gf)
        print(*fgf[0])
        print(*fgf[1])
        print(*fgf[2])

