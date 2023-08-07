from ...const import BOARD_SIZE, I_COUNT, L_COUNT


def movable(self, pos, ppos=None, opos=(0, 0)):
    x, y = pos
    if not ppos:
        (px, py) = self.position()
        (ox, oy) = self.position(1)
    else:
        px, py = ppos
        ox, oy = opos
    if x < 1 or x > BOARD_SIZE or y < 1 or y > BOARD_SIZE:
        return False
    dis = abs(px - x) + abs(py - y)
    if dis > 2 or dis == 0:
        return False
    elif dis == 1:
        if x == px:
            if self.vertical_block(x, max(y, py)):
                return False
        elif self.horizontal_block(max(x, px), y):
            return False
    else:
        if x == px:
            yt = oy
            if ox != x or yt * 2 != y + py:
                return False
            if self.vertical_block(x, yt) or self.vertical_block(x, yt + 1):
                return False
        elif y == py:
            xt = ox
            if oy != y or xt * 2 != x + px:
                return False
            if self.horizontal_block(xt, y) or self.horizontal_block(xt + 1, y):
                return False
        elif px == ox and y == oy:
            if abs(x - px) != 1 or \
                    self.vertical_block(px, max(y, py)) or \
                    self.horizontal_block(max(x, px), y) or \
                    not self.vertical_block(px, y + 1 if y > py else y):
                return False
        elif py == oy and x == ox:
            if abs(y - py) != 1 or \
                    self.vertical_block(x, max(y, py)) or \
                    self.horizontal_block(max(x, px), y) or \
                    not self.horizontal_block(x + 1 if x > px else x, py):
                return False
        else:
            return False

    if ox == x and oy == y and not self.internal():
        return False

    return True
