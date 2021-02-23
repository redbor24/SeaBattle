from random import randint

# Размерность доски
BOARD_SIZE = 10


# Возвращает обрамлённую служебными строками переданную строку для вывода её в консоль указанным цветом
def colorized(s, c):
    if c == "red":
        return f"\u001b[38;5;9m{s}\u001b[0m"  # 9 - красный
    elif c == "dark-green":
        return f"\u001b[38;5;22m{s}\u001b[0m"  # 22 - тёмно-зелёный
    elif c == "light-green":
        return f"\u001b[38;5;46m{s}\u001b[0m"  # 46 - ярко-зелёный
    elif c == "blue":
        return f"\u001b[38;5;14m{s}\u001b[0m"  # 14 - голубой
    else:
        return f"\u001b[0m{s}\u001b[0m"


def alive_deck():
    return colorized("■", "light-green")


def shooted_deck():
    return colorized("X", "red")


def shooted_free_cell():
    return colorized(chr(183), "blue")


def free_cell(debug=False):
    if debug:
        return colorized("T", "dark-green")
    else:
        return colorized(chr(183), "dark-green")


def contour_cell():
    return colorized(chr(183), "blue")


# Exceptions
class BoardExceptions(Exception):
    """
    Базовое исключение для игры
    """
    pass


class OutOfBoard(BoardExceptions):
    """
    Выбрасывается при выходе за пределы игровой доски
    """
    def __str__(self):
        return colorized("Ошибка! Выстрел за пределы доски!", "red")
        # return "Выстрел за пределы доски!"


class BadBoard(BoardExceptions):
    """
    Выбрасывается при некорректном размере игровой доски
    """
    def __str__(self):
        return colorized("Ошибка! Задайте правильный размер игровой доски!", "red")


class BoardUsed(BoardExceptions):
    """
    Выбрасывается при повторном выстреле в клетку
    """
    def __str__(self):
        return colorized("Ошибка! В эту клетку уже стреляли!", "red")


class BadShip(BoardExceptions):
    """
    Выбрасываается при невозможности размещения корабля
    """
    def __str__(self):
        return colorized("Ошибка! Здесь нельзя расположить этот корабль!", "red")


# Dot
class Dot:
    """
    "Игровая точка"
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

    def __str__(self):
        return self.__repr__()


# Ship
class Ship():
    def __init__(self, start, size, direction):
        self.start = start  # стартовая точка корабля
        self.size = size  # размер корабля (количество палуб)
        self.direction = direction  # направление корабля (ориентация): 0 - вертикально, 1 - горизонтально
        self.lives = size  # оставшееся количество жизней корабля. Изначально равно количеству палуб

    @property
    def dots(self):
        ship_dots = []
        cur_x = self.start.x
        cur_y = self.start.y
        for i in range(self.size):
            ship_dots.append(Dot(cur_x, cur_y))
            if self.direction == 0:
                cur_x += 1
            elif self.direction == 1:
                cur_y += 1
        return ship_dots

    def shooted(self, shot):
        return shot in self.dots


# Board
class Board():
    def __init__(self, is_hide=False, size=0):
        self.size = size
        if size == 0:
            raise BadBoard()
        self.is_hide = is_hide
        self.shooted_ships = 0  # Количество поражённых кораблей на доске

        # Инициализация игрового массива
        self.field = [[free_cell()] * size for _ in range(size)]
        self.busy = []  # Непустые клетки
        self.ships = []  # Корабли доски

    @property
    def ship_count(self):
        return len(self.ships)

    def __str__(self):
        res = " " * 5
        # Номера столбцов
        for i, row in enumerate(self.field):
            res += f" {str(i + 1)}"
        res += " \n" + " " * 5
        # Разделитель
        for i, row in enumerate(self.field):
            res += "--"
        res += "--"
        # Строки игровой доски
        for i, row in enumerate(self.field):
            res += f"\n{str.rjust(str(i + 1), 3)} | " + " ".join(row) + " |"

        if self.is_hide:
            res = res.replace("■", free_cell())
        return res

    def is_out(self, dot):
        return not(0 <= dot.x <= self.size - 1 and 0 <= dot.y <= self.size - 1)

    def is_busy(self, dot):
        return dot in self.busy

    def contour(self, ship, is_show=False):
        near_dots = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for dx, dy in near_dots:
                cur_dot = Dot(dot.x + dx, dot.y + dy)
                if not(self.is_out(cur_dot)) and cur_dot not in self.busy and cur_dot not in ship.dots:
                    self.busy.append(cur_dot)
                    # Показываем контур, если надо
                    if is_show:
                        self.field[cur_dot.x][cur_dot.y] = contour_cell()

    def add_ship(self, ship):
        #  Проверяем точки корабля на корректность кооординат
        for dot in ship.dots:
            if self.is_out(dot) or dot in self.busy:
                raise BadShip()
        # Точки корабля
        for dot in ship.dots:
            # на игровом поле помечаем как палубу
            self.field[dot.x][dot.y] = alive_deck()
            # и добавляем в список занятых точек
            self.busy.append(dot)

        self.ships.append(ship)
        # self.contour(ship, True)
        self.contour(ship)

    def shot(self, dot):
        """
        Выстрел в точку :param dot:
        :return: Возвращает True или False как ответ на вопрос - нужно ли повторить ход
        """

        if self.is_out(dot):
            raise OutOfBoard()

        if self.is_busy(dot):
            raise BoardUsed()

        self.busy.append(dot)
        for ship in self.ships:
            if ship.shooted(dot):
                ship.lives -= 1
                self.field[dot.x][dot.y] = shooted_deck()
                # Если у корабля кончились жизни, то
                if ship.lives == 0:
                    # Увеличиваем счётчик уничтоженных кораблей на доске
                    self.shooted_ships += 1
                    # Рисуем контур вокруг уничтоженного корабля
                    self.contour(ship, is_show=True)
                    print("Корапь утоп")
                    # return False
                else:
                    print("Корапь ранен")
                return True

        self.field[dot.x][dot.y] = shooted_free_cell()
        print("Мазила!")
        return False

    def begin(self):
        self.busy = []


class Player():
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
    def __init__(self, size=0, ship_lens=[]):
        self.size = size
        self.ship_lens = ship_lens
        human_board = self.random_board()
        comp_board = self.random_board()
        comp_board.is_hide = False  # True
        self.__koeff = (size * 2 + 10) * 2

        self.ai = AI(comp_board, human_board)
        self.user = Human(human_board, comp_board)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
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
        print(str.center("Вы", 30) + ":: " + str.center("Компьютер", 30))

        human_board_str = str(self.user.self_board).split("\n")
        comp_board_str = str(self.ai.self_board).split("\n")
        res_str = ""
        for i in range(len(human_board_str)):
            res_str += human_board_str[i] + "   :: " + comp_board_str[i] + "\n"
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
