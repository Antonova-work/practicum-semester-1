'''
Реализовать программу, при помощи которой двое пользователей могут
играть в игру «Супер ним». Правила игры следующие. На
шахматной доске в некоторых клетках случайно разбросаны фишки или
пуговицы. Игроки ходят по очереди. За один ход можно снять все фишки с
какой-либо горизонтали или вертикали, на которой они есть. Выигрывает
тот, кто заберет последние фишки. Взаимодействие с программой
производится через консоль. Игровое поле изображается в виде текстовых
строк и перерисовывается при каждом изменении состояния поля. При
запросе данных от пользователя программа сообщает, что ожидает от
пользователя (в частности, координаты новой отметки на поле) и проверяет
корректность ввода. Программа должна уметь автоматически определять,
что партия окончена, и сообщать о победе одного из игроков. Сама
программа НЕ ходит, т.е. не пытается выбирать строки или столбцы с
целью победить в игре.
'''

import random


alphabet = 'abcdefgh'
array = [
    [
        "○" for i in range(8)
    ] for j in range(1, 8 + 1)
]

def _random_amount_button():
    random_number = random.randint(1, 64) #количество фишек на поле.
    return random_number


def place_random_buttons():
    random_number = _random_amount_button() #Получение случайного количества фишек.
    for i in range(random_number):
        random_row = random.randint(0, 7) #Выбираются случайные координаты клетки (строка и столбец от 0 до 7).
        random_col = random.randint(0, 7)
        array[random_row][random_col] = '●' #В выбранную клетку записывается символ фишка.


def _remove_row(selected_row: str): #Функции для выполнения хода 
    row_index = alphabet.find(selected_row) #Преобразование буквы в числовой индекс строки с помощью поиска в строке alphabet.
    for element_index in range(0, len(array[row_index])): #Цикл по всем элементам выбранной строки. Каждый элемент заменяется на "○", очищая всю строку.
        array[row_index][element_index] = "○"


def _remove_column(selected_column: int):
    column_index = selected_column - 1 #Преобразование номера столбца в индекс массива.
    for row_index in range(8): #Цикл по всем строкам игрового поля. Для каждой строки элемент в выбранном столбце заменяется на "○", очищая весь столбец.
        array[row_index][column_index] = "○"


def select_move():
    move = input('Выберите столбец (a-h)/ряд (1-8): ')
    make_move(move)


def check_row(selected_row: str):
    row_index = alphabet.find(selected_row) #Поиск индекса строки по букве.
    if "●" in array[row_index]: #Проверка наличия хотя бы одной фишки ("●") в указанной строке. Возвращает True, если фишки есть.
        return True
    return False


def check_column(selected_column: int):
    column_index = selected_column - 1 # Преобразование номера столбца в индекс.
    for row_index in range(8): #Цикл по всем строкам. Если в какой-либо строке найден столбец с фишкой, сразу возвращается True.
        if array[row_index][column_index] == "●":
            return True
    return False


def make_move(move): 
    if move == "": #Проверка на пустой ввод.
        select_move()
    try: #Попытка преобразовать ввод в целое число. Если успешно — пользователь, вероятно, ввел номер столбца.
        move = int(move)
        if (1 <= move <= 8) and check_column(move): #Если проверка пройдена, очищается столбец.
            _remove_column(move)
        else: #Если проверка не пройдена, ход считается невалидным, и функция select_move вызывается снова.
            select_move()
    except ValueError:
        if (move in alphabet) and (check_row(move)): #Проверка, что буква есть в alphabet и в строке есть фишки.
            _remove_row(move) #Если проверка пройдена, очищается строка.
        else:#Если проверка не пройдена, ход считается невалидным.
            select_move()


def check_array():
    """
    Двойной цикл по всем клеткам поля. Если встречается хотя бы одна непустая клетка (не "○"), 
    функция сразу возвращает True (фишки еще есть). 
    Если все клетки пусты, возвращает False (игра окончена).
    """
    for row in array:
        for element in row:
            if element == "○":
                continue
            else:
                return True
    return False


def process_game_moves(current_move: int):
    if current_move == 0: #Корректировка номера хода для красивого отображения (чтобы игроки были 1 и 2, а не 0 и 1).
        current_move = 2
    fisrt_player_move = input(f"Ход {current_move} игрока: ") #Запрос хода у текущего игрока.
    make_move(fisrt_player_move)
    make_pretty_field()
    result = current_move # Сохранение номера текущего игрока в переменную result (это будет победитель, если ход был последним).
    if check_array(): #Проверка, остались ли фишки на поле.
        current_move = (current_move + 1) % 2
        result = process_game_moves(current_move)
    return result #Когда фишек не осталось (check_array() вернула False), функция возвращает номер игрока, который только что походил (то есть победителя).


def make_pretty_field():
    """
    Форматирует игровое поле в приятный для игры вид.
    """
    print('–––––––––––––––––––––')
    index = 0
    for row in array:
        print(alphabet[index], "|", *row, "|")
        index += 1
    print("––––––––––––––––––– |")
    print("  |", *[str(i) for i in range(1, 8 + 1)], "|")
    print('––––––––––––––––––– |')


def game():
    """
    Запускает игру.
    """
    print("Здравствуйте! Играйте.")
    place_random_buttons() #Случайная расстановка фишек на поле.
    make_pretty_field() #Первоначальная отрисовка поля.
    current_move = 1 #Определение, что первым ходит игрок №1.
    winner = process_game_moves(current_move) #Запуск основного игрового цикла через вызов process_game_moves. Функция завершится, когда игра закончится, и вернет номер победителя.
    print(f'Игра окончена! Победил {winner} игрок!')


game()