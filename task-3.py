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

import logging
import random

logger = logging.getLogger()
logger.setLevel(logging.WARN)

alphabet = 'abcdefgh'
array = [
    [
        "○" for _ in range(8)
    ] for _ in range(1, 8 + 1)
]


def _random_amount_button() -> int:
    """
    Генерирует случайное кол-во пуговиц
    """
    random_number = random.randint(1, 64)
    logger.debug(f'Random number: {random_number}')
    return random_number


def place_random_buttons():
    """
    Ставит в случайном порядке пуговицы на игровое поле.
    """
    random_number = _random_amount_button()
    for i in range(random_number):
        random_row = random.randint(0, 7)
        random_col = random.randint(0, 7)
        array[random_row][random_col] = '●'


def _remove_row(selected_row: str) -> None:
    """
    Очищает ряд с игрового поля (массива).
    selected_row: – выбранный ряд
    """
    row_index = alphabet.find(selected_row)
    logger.debug(row_index)
    for element_index in range(0, len(array[row_index])):
        array[row_index][element_index] = "○"


def _remove_column(selected_column: int) -> None:
    """
    Очищает столбец с игрового поля (массива).
    selected_column: – выбранный столбец
    """
    column_index = selected_column - 1
    logger.debug(column_index)
    for row_index in range(8):
        array[row_index][column_index] = "○"


def select_move():
    move = input('Выберите столбец (a-h)/ряд (1-8): ')
    make_move(move)


def check_row(selected_row: str) -> bool:
    """
    Проверяет, есть ли в ряду пуговицы
    selected_row: выбранный ряд (a-h)
    """
    row_index = alphabet.find(selected_row)
    logger.debug(row_index)
    if "●" in array[row_index]:
        return True
    return False


def check_column(selected_column: int) -> bool:
    """
    Проверяет, есть ли в столбце пуговицы
    selected_column: выбранный столбец (1-8)
    """
    column_index = selected_column - 1
    logger.debug(column_index)
    for row_index in range(8):
        if array[row_index][column_index] == "●":
            return True
    return False


def make_move(move):
    """
    Определяет выбранный ход пользователя и удаляет пуговицы с игрового поля.
    move: – ход
    """
    if move == "":
        logger.debug("Invalid move")
        select_move()
    try:
        move = int(move)
        if (1 <= move <= 8) and check_column(move):
            _remove_column(move)
        else:
            logger.debug("Invalid move")
            select_move()
    except ValueError:
        if (move in alphabet) and (check_row(move)):
            _remove_row(move)
        else:
            logger.debug("Invalid move")
            select_move()


def check_array() -> bool:
    """
    Проверяет, имеет ли игровое поле внутри себя пуговицы.
    """
    for row in array:
        for element in row:
            if element == "○":
                continue
            else:
                return True
    return False


def process_game_moves(current_move: int) -> int:
    """
    Рекурсивная функция, отвечающая за процесс игры.

    Если игровое поле (массив) ещё имеет пуговицы, то игра продолжается
    current_move: – 123
    return: Последнего игрока (победителя)
    """
    if current_move == 0:
        current_move = 2
    fisrt_player_move = input(f"Ход {current_move} игрока: ")
    make_move(fisrt_player_move)
    make_pretty_field()
    result = current_move
    if check_array():
        current_move = (current_move + 1) % 2
        result = process_game_moves(current_move)
    return result


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
    place_random_buttons()
    make_pretty_field()
    current_move = 1
    winner = process_game_moves(current_move)
    print(f'Игра окончена! Победил {winner} игрок!')


game()