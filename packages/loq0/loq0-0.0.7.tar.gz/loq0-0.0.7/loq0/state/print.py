class colors:
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ENDC = '\033[0m'


def bold_sym(s: str):
    return "╋" if s == "┼" else "┃" if s == "│" else "━━━" if s == "───" else s


def __str__(self):
    if self.st[0, 2] == 0:
        (px, py), (ox, oy) = self.position(), self.position(1)
    else:
        (px, py), (ox, oy) = self.position(1), self.position()

    res = ''
    board = [[("┼" if y % 2 else "│") if x % 2 else ("───" if y % 2 else "   ") for x in range(17)] for y in range(17)]

    board[2 * (py - 1)][2 * (px - 1)] = f'{colors.BLUE} O {colors.ENDC}'
    board[2 * (oy - 1)][2 * (ox - 1)] = f'{colors.RED} O {colors.ENDC}'

    def hl(x, y):
        if x >= 0 and x < 17 and y >= 0 and y < 17:
            board[y][x] = bold_sym(board[y][x])

    for wall_i in self.st[2:16]:
        wx, wy, opt = wall_i
        wx = 2 * wx - 1
        wy = 2 * wy - 1
        if opt == 1:
            for ty in [wy - 1, wy, wy + 1]:
                hl(wx - 2, ty)
        elif opt == 2:
            for tx in [wx - 1, wx, wx + 1]:
                hl(tx, wy - 2)

    for wall_l in self.st[16:]:
        wx, wy, opt = wall_l
        wx = 2 * wx - 1
        wy = 2 * wy - 1
        if opt == 1:
            for x, y in [(wx - 1, wy - 2), (wx - 2, wy - 2), (wx - 2, wy - 1)]: hl(x, y)
        elif opt == 2:
            for x, y in [(wx - 1, wy), (wx - 2, wy), (wx - 2, wy - 1)]: hl(x, y)
        elif opt == 3:
            for x, y in [(wx - 1, wy), (wx, wy), (wx, wy - 1)]: hl(x, y)
        elif opt == 4:
            for x, y in [(wx - 1, wy - 2), (wx, wy - 2), (wx, wy - 1)]: hl(x, y)

    for i, line in enumerate(board):
        res = f'  {"".join(line)}{colors.CYAN}{(i + 2) // 2 if not i % 2 else " "}{colors.ENDC}\n' + res

    res += f'   {"   ".join(map(lambda i: f"{colors.GREEN}{i}{colors.ENDC}", range(1, 10)))}'
    return res
