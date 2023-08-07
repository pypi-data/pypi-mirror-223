import numpy as np
from ..const import BOARD_SIZE, I_COUNT, L_COUNT


class State:
    def __init__(self, state=None, dtype=np.uint8):
        if state is None:
            self.st = np.zeros((2 + (I_COUNT + L_COUNT) * 2, 3), dtype=dtype)
            self.st[0, 0] = (BOARD_SIZE + 1) // 2
            self.st[0, 1] = 1
            self.st[1, 0] = (BOARD_SIZE + 1) // 2
            self.st[1, 1] = BOARD_SIZE
        else:
            self.st = state

    def copy(self):
        return State(self.st.copy())

    def player(self, op=None):
        if op is None:
            return self.st[0, 2]
        return 1 - self.st[0, 2]

    def internal(self, op=None):
        pl = self.player()
        return 4 <= self.st[pl, 0] <= 6 and 4 <= self.st[pl, 1] <= 6

    def i_walls(self):
        return self.st[2 + np.array(*np.where(self.st[2:2 + I_COUNT * 2, 0] != 0)), :]

    def l_walls(self):
        return self.st[2 + I_COUNT * 2 + np.array(*np.where(self.st[2 + I_COUNT * 2:, 0] != 0)), :]

    def position(self, op=None):
        pl = self.player(op)
        return self.st[pl, 0], self.st[pl, 1]

    def win(self):
        if self.st[0, 1] == BOARD_SIZE:
            return 0
        elif self.st[1, 1] == 1:
            return 1
        return None

    from .validate.blocked import horizontal_block, vertical_block
    from .validate.movable import movable
    from .validate.endable import endable
    from .validate.cross import cross
    from .validate.internal import block_internal

    from .actions import move, place_i, place_l
    from .actions import act
    from .print import __str__
