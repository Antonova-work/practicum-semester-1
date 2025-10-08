import random
import os
 
class BattleshipGame:
    def __init__(self):
        self.board_size = 10
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  
        self.player_board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.shot_board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ship_positions = []
        self.remaining_ships = len(self.ships)
        self.total_cells = sum(self.ships)
        self.hit_cells = 0
        self.last_message = ""
 
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
 
    def is_valid_position(self, row, col, length, direction):
        if direction == 'H':  
            if col + length > self.board_size:
                return False
            for i in range(max(0, row-1), min(self.board_size, row+2)):
                for j in range(max(0, col-1), min(self.board_size, col+length+1)):
                    if self.player_board[i][j] != '~':
                        return False
        else: 
            if row + length > self.board_size:
                return False
            for i in range(max(0, row-1), min(self.board_size, row+length+1)):
                for j in range(max(0, col-1), min(self.board_size, col+2)):
                    if self.player_board[i][j] != '~':
                        return False
        return True
 
    def place_ship(self, row, col, length, direction):
        positions = []
        if direction == 'H':  
            for j in range(col, col + length):
                self.player_board[row][j] = 'O'  
                positions.append((row, j))
        else:  
            for i in range(row, row + length):
                self.player_board[i][col] = 'O'
                positions.append((i, col))
        self.ship_positions.append(positions)
 
    def generate_ships(self):
        for ship_length in self.ships:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                direction = random.choice(['H', 'V'])
                if direction == 'H':
                    row = random.randint(0, self.board_size - 1)
                    col = random.randint(0, self.board_size - ship_length)
                else:
                    row = random.randint(0, self.board_size - ship_length)
                    col = random.randint(0, self.board_size - 1)
 
                if self.is_valid_position(row, col, ship_length, direction):
                    self.place_ship(row, col, ship_length, direction)
                    placed = True
                attempts += 1
 
            if not placed:
                self.player_board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
                self.ship_positions = []
                self.generate_ships()
                return
 
    def display_board(self):
        self.clear_screen()
        print()
        print("МОРСКОЙ БОЙ")
        print()
 
        if self.last_message:
            print(f"\n{self.last_message}")
 
        print("\nВаше поле (где вы стреляете):")
        print("  ~ - неизвестно | X - попадание | • - промах")
        print()
 
        print("   " + " ".join(str(i) for i in range(1, self.board_size + 1)))
 
        letters = 'АБВГДЕЖЗИК'
        for i in range(self.board_size):
            row_display = []
            for j in range(self.board_size):
                cell = self.shot_board[i][j]
                row_display.append(cell)
            print(f"{letters[i]}  {' '.join(row_display)}")
 
        print(f"\nОсталось кораблей: {self.remaining_ships}")
        print(f"Попаданий: {self.hit_cells}/{self.total_cells}")
        print("\n" + "="*30)
 
    def get_coordinates(self, input_str):
        if len(input_str) < 2:
            return None, None
 
        letter = input_str[0].upper()
        letters = 'АБВГДЕЖЗИК'
        if letter not in letters:
            return None, None
 
        row = letters.index(letter)
 
        try:
            col = int(input_str[1:]) - 1  
        except ValueError:
            return None, None
 
        if col < 0 or col >= self.board_size:
            return None, None
 
        return row, col
 
    def check_ship_sunk(self, row, col):
        for ship in self.ship_positions:
            if (row, col) in ship:
                for ship_row, ship_col in ship:
                    if self.shot_board[ship_row][ship_col] != 'X':
                        return False
                return True
        return False
 
    def mark_sunk_ship(self, ship):
        for row, col in ship:
            for i in range(max(0, row-1), min(self.board_size, row+2)):
                for j in range(max(0, col-1), min(self.board_size, col+2)):
                    if self.shot_board[i][j] == '~':
                        self.shot_board[i][j] = '•' 
 
    def make_shot(self, row, col):
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return "недопустимые координаты!"
 
        if self.shot_board[row][col] != '~':
            return "вы уже стреляли в эту клетку!"
 
        if self.player_board[row][col] == 'O': 
            self.shot_board[row][col] = 'X'
            self.hit_cells += 1
 
            if self.check_ship_sunk(row, col):
                for ship in self.ship_positions:
                    if (row, col) in ship:
                        self.mark_sunk_ship(ship)
                        self.remaining_ships -= 1
                        return "ПОТОПЛЕН!"
                return "ПОТОПЛЕН!"
            else:
                return "ПОПАДАНИЕ!"
        else:  
            self.shot_board[row][col] = '•'
            return "ПРОМАХ!"
 
    def is_game_over(self):
        return self.hit_cells == self.total_cells
 
    def play(self):
        print("добро пожаловать в игру 'морской бой'!")
        print("компьютер случайным образом расставил корабли.")
        print("ваша задача - потопить все корабли противника!")
        print("\nправила ввода координат:")
        print("  - введите букву строки (А-К) и номер столбца (1-10)")
        print("  - например: 'А1', 'В5', 'К10'")
        print("\nнажмите Enter чтобы начать...")
        input()
 
        self.generate_ships()
        self.last_message = "игра началась! сделайте первый выстрел."
 
        while not self.is_game_over():
            self.display_board()
            print("введите координаты для выстрела:")
            user_input = input("> ").strip()
 
            if user_input.upper() in ['ВЫХОД', 'EXIT', 'QUIT']:
                print("игра завершена.")
                return
 
            row, col = self.get_coordinates(user_input)
 
            if row is None or col is None:
                self.last_message = "ошибка! введите координаты в формате 'А1', 'В5' и т.д. (буквы: А-К, цифры: 1-10)"
                continue
 
            result = self.make_shot(row, col)
            letters = 'АБВГДЕЖЗИК'
            coord_str = f"{letters[row]}{col+1}"
            self.last_message = f"выстрел в {coord_str}: {result}"
 
            if self.is_game_over():
                break
 
        self.display_board()
        print("\n" + "="*50)
        print("ПОЗДРАВЛЯЮ! ВЫ ВЫИГРАЛИ!")
        print(f"вы потопили все {len(self.ships)} кораблей за {self.hit_cells + sum(1 for row in self.shot_board for cell in row if cell == '•')} выстрелов!")
        print("="*50)
        input("\nнажмите Enter чтобы продолжить...")
 
def main():
    while True:
        game = BattleshipGame()
        game.play()
 
        print("\nхотите сыграть еще раз? (да/нет)")
        play_again = input("> ").strip().lower()
        if play_again not in ['да', 'д', 'yes', 'y']:
            print("спасибо за игру! до свидания!")
            break
 
if __name__ == "__main__":
    main()
