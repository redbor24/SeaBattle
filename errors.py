from common import colorized


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
    def __init__(self, message="Ошибка! Выстрел за пределы доски!"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return colorized(self.message, "red")


class BadBoard(BoardExceptions):
    """
    Выбрасывается при некорректном размере игровой доски или при невозможности расставить корабли на доске
    """
    def __init__(self, message="Ошибка! Задайте правильный размер игровой доски!"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return colorized(self.message, "red")


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
    def __init__(self, message="Ошибка! Здесь нельзя расположить этот корабль!"):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return colorized(self.message, "red")
