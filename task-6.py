'''
МОРСКОЙ БОЙ
'''
'''
Реализовать программу, с которой можно играть в игру «Морской бой».
Программа автоматически случайно расставляет на поле размером 10 на
10 клеток: четыре однопалубных корабля, три двухпалубных корабля, два
трехпалубных корабля и один четырехпалубный. Между любыми двумя
кораблями по горизонтали и вертикали должна быть как минимум одна
незанятая клетка. Программа позволяет игроку ходить, производя
выстрелы. Сама программа НЕ ходит, т.е. не пытается топить корабли
расставленные игроком. Взаимодействие с программой производится через
консоль. Игровое поле изображается в виде десяти текстовых строк и
перерисовывается при каждом изменении состояния поля. При запросе
данных от пользователя программа сообщает, что ожидает от
пользователя (в частности, координаты очередного «выстрела») и
проверяет корректность ввода. Программа должна уметь автоматически
определять потопление корабля и окончание партии и сообщать об этих
событиях.
'''

import random
import os
 
class BattleshipGame:
    def __init__(self):
        # Инициализация игры
        self.board_size = 10  # Размер игрового поля 10x10
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Длины кораблей (1x4, 2x3, 3x2, 4x1)
        self.player_board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]  # Поле игрока с кораблями
        self.shot_board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]  # Поле для отметок выстрелов
        self.ship_positions = []  # Список позиций всех кораблей
        self.remaining_ships = len(self.ships)  # Количество оставшихся кораблей
        self.total_cells = sum(self.ships)  # Общее количество клеток, занимаемых кораблями
        self.hit_cells = 0  # Количество попаданий
        self.last_message = ""  # Сообщение о результате последнего выстрела
 
    def clear_screen(self):
        # Очистка экрана консоли
        os.system('cls' if os.name == 'nt' else 'clear')
 
    def is_valid_position(self, row, col, length, direction):
        # Проверка возможности размещения корабля в указанной позиции
        if direction == 'H':  # Горизонтальное размещение
            if col + length > self.board_size:  # Корабль выходит за границы поля
                return False
            # Проверка области вокруг корабля (включая соседние клетки)
            for i in range(max(0, row-1), min(self.board_size, row+2)):
                for j in range(max(0, col-1), min(self.board_size, col+length+1)):
                    if self.player_board[i][j] != '~':  # Если клетка уже занята
                        return False
        else:  # Вертикальное размещение
            if row + length > self.board_size:  # Корабль выходит за границы поля
                return False
            # Проверка области вокруг корабля (включая соседние клетки)
            for i in range(max(0, row-1), min(self.board_size, row+length+1)):
                for j in range(max(0, col-1), min(self.board_size, col+2)):
                    if self.player_board[i][j] != '~':  # Если клетка уже занята
                        return False
        return True  # Позиция допустима
 
    def place_ship(self, row, col, length, direction):
        # Размещение корабля на поле
        positions = []  # Список для хранения позиций корабля
        if direction == 'H':  # Горизонтальное размещение
            for j in range(col, col + length):
                self.player_board[row][j] = 'O'  # 'O' обозначает корабль
                positions.append((row, j))
        else:  # Вертикальное размещение
            for i in range(row, row + length):
                self.player_board[i][col] = 'O'
                positions.append((i, col))
        self.ship_positions.append(positions)  # Добавляем корабль в список
 
    def generate_ships(self):
        # Автоматическая расстановка всех кораблей на поле
        for ship_length in self.ships:
            placed = False  # Флаг успешного размещения корабля
            attempts = 0  # Счетчик попыток размещения
            while not placed and attempts < 100:  # До 100 попыток на корабль
                # Случайный выбор направления и позиции
                direction = random.choice(['H', 'V'])
                if direction == 'H':
                    row = random.randint(0, self.board_size - 1)
                    col = random.randint(0, self.board_size - ship_length)  # Учитываем длину корабля
                else:
                    row = random.randint(0, self.board_size - ship_length)
                    col = random.randint(0, self.board_size - 1)
 
                if self.is_valid_position(row, col, ship_length, direction):
                    self.place_ship(row, col, ship_length, direction)
                    placed = True  # Корабль успешно размещен
                attempts += 1
 
            if not placed:
                # Если не удалось разместить корабль, начинаем расстановку заново
                self.player_board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
                self.ship_positions = []
                self.generate_ships()
                return
 
    def display_board(self):
        # Отображение игрового интерфейса
        self.clear_screen()
        print()
        print("МОРСКОЙ БОЙ")
        print()
 
        if self.last_message:
            print(f"\n{self.last_message}")  # Показываем результат последнего выстрела
 
        print("\nВаше поле (где вы стреляете):")
        print("  ~ - неизвестно | X - попадание | • - промах")
        print()
 
        # Отображение номеров столбцов (1-10)
        print("   " + " ".join(str(i) for i in range(1, self.board_size + 1)))
 
        # Отображение поля с буквенными обозначениями строк (А-К)
        letters = 'АБВГДЕЖЗИК'
        for i in range(self.board_size):
            row_display = []
            for j in range(self.board_size):
                cell = self.shot_board[i][j]
                row_display.append(cell)
            print(f"{letters[i]}  {' '.join(row_display)}")  # Буква строки и клетки
 
        # Отображение статистики игры
        print(f"\nОсталось кораблей: {self.remaining_ships}")
        print(f"Попаданий: {self.hit_cells}/{self.total_cells}")
        print("\n" + "="*30)
 
    def get_coordinates(self, input_str):
        # Преобразование ввода пользователя в координаты поля
        if len(input_str) < 2:
            return None, None
 
        letter = input_str[0].upper()  # Первый символ - буква строки
        letters = 'АБВГДЕЖЗИК'  # Допустимые буквы
        if letter not in letters:
            return None, None
 
        row = letters.index(letter)  # Преобразуем букву в номер строки
 
        try:
            col = int(input_str[1:]) - 1  # Остальные символы - номер столбца (переводим в 0-based)
        except ValueError:
            return None, None
 
        if col < 0 or col >= self.board_size:  # Проверка границ
            return None, None
 
        return row, col
 
    def check_ship_sunk(self, row, col):
        # Проверка, потоплен ли корабль после попадания
        for ship in self.ship_positions:
            if (row, col) in ship:  # Находим корабль, в который попали
                # Проверяем, все ли клетки корабля подбиты
                for ship_row, ship_col in ship:
                    if self.shot_board[ship_row][ship_col] != 'X':  # Если есть неподбитая клетка
                        return False
                return True  # Все клетки корабля подбиты
        return False
 
    def mark_sunk_ship(self, ship):
        # Отмечаем область вокруг потопленного корабля промахами
        for row, col in ship:
            # Проверяем все соседние клетки вокруг каждой клетки корабля
            for i in range(max(0, row-1), min(self.board_size, row+2)):
                for j in range(max(0, col-1), min(self.board_size, col+2)):
                    if self.shot_board[i][j] == '~':  # Если клетка не отмечена
                        self.shot_board[i][j] = '•'  # Отмечаем как промах
 
    def make_shot(self, row, col):
        # Выполнение выстрела по указанным координатам
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return "недопустимые координаты!"
 
        if self.shot_board[row][col] != '~':  # Проверка, не стреляли ли уже сюда
            return "вы уже стреляли в эту клетку!"
 
        if self.player_board[row][col] == 'O':  # Попадание в корабль
            self.shot_board[row][col] = 'X'  # Отмечаем попадание
            self.hit_cells += 1
 
            # Проверяем, потоплен ли корабль
            if self.check_ship_sunk(row, col):
                for ship in self.ship_positions:
                    if (row, col) in ship:
                        self.mark_sunk_ship(ship)  # Отмечаем область вокруг потопленного корабля
                        self.remaining_ships -= 1  # Уменьшаем счетчик кораблей
                        return "ПОТОПЛЕН!"
                return "ПОТОПЛЕН!"
            else:
                return "ПОПАДАНИЕ!"
        else:  # Промах
            self.shot_board[row][col] = '•'  # Отмечаем промах
            return "ПРОМАХ!"
 
    def is_game_over(self):
        # Проверка окончания игры (все корабли потоплены)
        return self.hit_cells == self.total_cells
 
    def play(self):
        # Основной игровой цикл
        print("добро пожаловать в игру 'морской бой'!")
        print("компьютер случайным образом расставил корабли.")
        print("ваша задача - потопить все корабли противника!")
        print("\nправила ввода координат:")
        print("  - введите букву строки (А-К) и номер столбца (1-10)")
        print("  - например: 'А1', 'В5', 'К10'")
        print("\nнажмите Enter чтобы начать...")
        input()
 
        self.generate_ships()  # Расставляем корабли
        self.last_message = "игра началась! сделайте первый выстрел."
 
        while not self.is_game_over():  # Пока игра не окончена
            self.display_board()  # Показываем поле
            print("введите координаты для выстрела:")
            user_input = input("> ").strip()  # Получаем ввод пользователя
 
            if user_input.upper() in ['ВЫХОД', 'EXIT', 'QUIT']:  # Проверка на выход
                print("игра завершена.")
                return
 
            row, col = self.get_coordinates(user_input)  # Преобразуем ввод в координаты
 
            if row is None or col is None:  # Если координаты невалидны
                self.last_message = "ошибка! введите координаты в формате 'А1', 'В5' и т.д. (буквы: А-К, цифры: 1-10)"
                continue
 
            # Выполняем выстрел и получаем результат
            result = self.make_shot(row, col)
            letters = 'АБВГДЕЖЗИК'
            coord_str = f"{letters[row]}{col+1}"  # Форматируем координаты для вывода
            self.last_message = f"выстрел в {coord_str}: {result}"  # Сохраняем сообщение
 
            if self.is_game_over():  # Проверяем, не окончена ли игра
                break
 
        # Игра окончена - показываем результаты
        self.display_board()
        print("\n" + "="*50)
        print("ПОЗДРАВЛЯЮ! ВЫ ВЫИГРАЛИ!")
        # Подсчитываем общее количество выстрелов (попадания + промахи)
        print(f"вы потопили все {len(self.ships)} кораблей за {self.hit_cells + sum(1 for row in self.shot_board for cell in row if cell == '•')} выстрелов!")
        print("="*50)
        input("\nнажмите Enter чтобы продолжить...")
 
def main():
    # Главная функция программы
    while True:
        game = BattleshipGame()  # Создаем новую игру
        game.play()  # Запускаем игровой процесс
 
        # Предлагаем сыграть еще раз
        print("\nхотите сыграть еще раз? (да/нет)")
        play_again = input("> ").strip().lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("спасибо за игру! до свидания!")
            break
 
if __name__ == "__main__":
    main()  # Запускаем программу