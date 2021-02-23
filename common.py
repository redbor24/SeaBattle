# Состояния точки игрового поля
cell_state = {
    "FREE_CELL": {'value': "a", 'symbol': chr(183), 'color': "dark-green"},  # Свободная кас... клетка
    "USED_CELL": {'value': "b", 'symbol': chr(183), 'color': "blue"},  # Клетка,в которую уже стреляли
    "ALIVE_DECK": {'value': "c", 'symbol': "■", 'color': "light-green"},  # Живая палуба корабля
    "SHOOTED_DECK": {'value': "d", 'symbol': "■", 'color': "red"},  # Подстреленная палуба
}


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


