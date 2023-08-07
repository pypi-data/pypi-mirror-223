from ...const import BOARD_SIZE, I_COUNT, L_COUNT


def place_i(self, x, y, w):
    if w == 1:
        if x < 1 or x > BOARD_SIZE + 1 or y < 1 or y > BOARD_SIZE - 1: return None
    elif w == 2:
        if x < 1 or x > BOARD_SIZE - 1 or y < 1 or y > BOARD_SIZE + 1: return None
    else:
        return None
    idx = 2 + self.player() * I_COUNT
    fl = -1
    for i in range(I_COUNT):
        if self.st[idx + i, 0] == 0:
            fl = i
            break
    if fl == -1: return None
    if self.cross(1, x, y, w): return None
    if not self.internal() and self.block_internal(1, x, y, w): return None
    st = self.copy()
    st.st[idx + fl, 0] = x
    st.st[idx + fl, 1] = y
    st.st[0, 2] = 1 - st.st[0, 2]
    st.st[idx + fl, 2] = w
    if not st.endable(): return False
    return st


def place_l(self, x, y, w):
    if x < 1 or x > BOARD_SIZE or y < 1 or y > BOARD_SIZE: return None
    if w < 1 or w > 4: return None
    idx = 2 + 2 * I_COUNT + self.player() * L_COUNT
    fl = -1
    for i in range(L_COUNT):
        if self.st[idx + i, 0] == 0:
            fl = i
            break
    if fl == -1: return None
    if self.cross(2, x, y, w): return None
    if not self.internal() and self.block_internal(2, x, y, w): return None
    st = self.copy()
    st.st[idx + fl, 0] = x
    st.st[idx + fl, 1] = y
    st.st[0, 2] = 1 - st.st[0, 2]
    st.st[idx + fl, 2] = w
    if not st.endable(): return False
    return st
