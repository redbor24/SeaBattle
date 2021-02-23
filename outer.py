from random import randint
from inner import Dot, Ship, Board
from errors import *

# Размерность доски
BOARD_SIZE = 10


class Player:
    def __init__(self, board, enemy):
        self.self_board = board
        self.enemy_board = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardExceptions as e:
                print(e)


class AI(Player):
    def ask(self):
        dot = Dot(randint(0, BOARD_SIZE - 1), randint(0, BOARD_SIZE - 1))
        print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
        return dot


class Human(Player):
    def ask(self):
        while True:
            coords = input("Ваш ход (строка столбец): ").split()
            if len(coords) != 2:
                print("Неверный ввод! Требуются две координаты (строка столбец)")
                continue
            x, y = coords
            if not(x.isdigit()) or not(y.isdigit()):
                print("Неверный ввод! Требуются числа!")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=0, ship_lens=[], hide_enemy_ships=True):
        self.size = size
        self.ship_lens = ship_lens
        try:
            print("Инициализация поля игрока...")
            human_board = self.random_board()
            print("Инициализация поля AI...")
            comp_board = self.random_board()
            comp_board.is_hide = hide_enemy_ships
            self.__koeff = (size * 2 + 10) * 2

            self.ai = AI(comp_board, human_board)
            self.user = Human(human_board, comp_board)
            self.start()
        except BoardExceptions as e:
            print(e)

    def random_board(self):
        board = None
        attempts = 0
        while board is None:
            board = self.random_place()
            attempts += 1
            if attempts > 100:
                break
            print(".", end="")
        print("")

        if board is None:
            raise BadBoard("Ошибка! Не удалось сгенерировать поле. Измените размер и/или количество кораблей "
                           "и попробуйте снова")

        return board

    def random_place(self):
        board = Board(size=self.size)
        attempts = 0
        for l in self.ship_lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BadShip:
                    pass
            # print(f"  Корабль: {l}, Попытка: {attempts}")
        board.begin()
        return board

    def hello(self):
        self.__print_line()
        print(str.center("Приветствуем вас в игре морской бой", self.__koeff))
        self.__print_line()
        print("Формат ввода: x y (номер строки, номер столбца)")

    def __print_line(self, s: str = "*", color=None):
        if color is None:
            print(s * self.__koeff)
        else:
            print(colorized(s * self.__koeff, color))

    def __print_res(self, is_human_win: bool = True):
        if is_human_win:
            self.__print_line(color="light-green")
            s = colorized("**" + str.center("Вы выиграли !!!", self.__koeff - 4) + "**", "light-green")
            print(s)  # color = 46 - ярко-зелёный
            self.__print_line(color="light-green")
        else:
            self.__print_line(color="red")
            s = colorized("**" + str.center("Вы проиграли...", self.__koeff - 4) + "**", "red")
            print(s)
            self.__print_line(color="red")

    def __print_game(self):
        # Печать игровых досок рядом, а не одна под другой
        self.__print_line()
        print(str.center("ИГРА", self.__koeff))
        self.__print_line()
        print(str.center("Вы", int(self.__koeff / 2)) + ":: " + str.center("Компьютер", int(self.__koeff / 2)))

        human_board_str = str(self.user.self_board).split("\n")
        comp_board_str = str(self.ai.self_board).split("\n")
        res_str = ""
        for i in range(len(human_board_str)):
            res_str += human_board_str[i] + "   ::" + comp_board_str[i] + "\n"
        print(res_str, end="")
        self.__print_line()

    def loop(self):
        num = 0
        while True:
            self.__print_game()

            if num % 2 == 0:
                repeat = self.user.move()
            else:
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.self_board.shooted_ships == self.ai.self_board.ship_count:
                self.__print_game()
                self.__print_res(is_human_win=True)
                break

            if self.user.self_board.shooted_ships == self.user.self_board.ship_count:
                self.__print_game()
                self.__print_res(is_human_win=False)
                break
            num += 1

    def start(self):
        self.hello()
        self.loop()
