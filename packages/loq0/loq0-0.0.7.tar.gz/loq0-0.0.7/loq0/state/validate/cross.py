from ...const import BOARD_SIZE, I_COUNT, L_COUNT


def cross(self, t, x, y, w):
    if t == 1:
        if w == 1:
            for i in range(2, 2 + I_COUNT * 2):
                if self.st[i, 0] == x - 1 and self.st[i, 1] == y + 1 and self.st[i, 2] == 2: return True
            return self.horizontal_block(x, y) or self.horizontal_block(x + 1, y)
        elif w == 2:
            for i in range(2, 2 + I_COUNT * 2):
                if self.st[i, 0] == x + 1 and self.st[i, 1] == y - 1 and self.st[i, 2] == 1: return True
            return self.vertical_block(x, y) or self.vertical_block(x, y + 1)
        else:
            return True
    elif t == 2:
        if w == 1:
            for i in range(2 + I_COUNT * 2, 2 + (I_COUNT + L_COUNT) * 2):
                if self.st[i, 0] == x - 1 and self.st[i, 1] == y - 1 and self.st[i, 2] == 3: return True
            return self.vertical_block(x, y) or self.horizontal_block(x, y)
        elif w == 2:
            for i in range(2 + I_COUNT * 2, 2 + (I_COUNT + L_COUNT) * 2):
                if self.st[i, 0] == x - 1 and self.st[i, 1] == y + 1 and self.st[i, 2] == 4: return True
            return self.horizontal_block(x, y) or self.vertical_block(x, y + 1)
        elif w == 3:
            for i in range(2 + I_COUNT * 2, 2 + (I_COUNT + L_COUNT) * 2):
                if self.st[i, 0] == x + 1 and self.st[i, 1] == y + 1 and self.st[i, 2] == 1: return True
            return self.vertical_block(x, y + 1) or self.horizontal_block(x + 1, y)
        elif w == 4:
            for i in range(2 + I_COUNT * 2, 2 + (I_COUNT + L_COUNT) * 2):
                if self.st[i, 0] == x + 1 and self.st[i, 1] == y - 1 and self.st[i, 2] == 2: return True
            return self.horizontal_block(x + 1, y) or self.vertical_block(x, y)
        else:
            return True
    return True
