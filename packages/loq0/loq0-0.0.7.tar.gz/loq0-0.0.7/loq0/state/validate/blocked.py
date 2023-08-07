from ...const import BOARD_SIZE, I_COUNT, L_COUNT


def vertical_block(self, x, y):
    for i in range(2, 2 + I_COUNT * 2):
        if self.st[i, 1] == y and (self.st[i, 0] == x or self.st[i, 0] == x - 1) and self.st[i, 2] == 2:
            return True

    for i in range(2 + I_COUNT * 2, 2 + (I_COUNT + L_COUNT) * 2):
        if self.st[i, 2] == 1 and self.st[i, 0] == x and self.st[i, 1] == y:
            return True
        if self.st[i, 2] == 2 and self.st[i, 0] == x and self.st[i, 1] == y - 1:
            return True
        if self.st[i, 2] == 3 and self.st[i, 0] == x and self.st[i, 1] == y - 1:
            return True
        if self.st[i, 2] == 4 and self.st[i, 0] == x and self.st[i, 1] == y:
            return True

    return False


def horizontal_block(self, x, y):
    for i in range(2, 2 + I_COUNT * 2):
        if self.st[i, 0] == x and (self.st[i, 1] == y or self.st[i, 1] == y - 1) and self.st[i, 2] == 1:
            return True

    for i in range(2 + I_COUNT * 2, 2 + (I_COUNT + L_COUNT) * 2):
        if self.st[i, 2] == 1 and self.st[i, 0] == x and self.st[i, 1] == y:
            return True
        if self.st[i, 2] == 2 and self.st[i, 0] == x and self.st[i, 1] == y:
            return True
        if self.st[i, 2] == 3 and self.st[i, 0] == x - 1 and self.st[i, 1] == y:
            return True
        if self.st[i, 2] == 4 and self.st[i, 0] == x - 1 and self.st[i, 1] == y:
            return True

    return False
