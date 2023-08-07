ACTION_MOVE = 0
ACTION_PLACE_I = 1
ACTION_PLACE_L = 2

from .move import move
from .place import place_i, place_l


def act(self, t, p1, p2, p3=None):
    if t == ACTION_MOVE:
        return self.move(p1, p2)
    if t == ACTION_PLACE_I:
        return self.place_i(p1, p2, p3)
    if t == ACTION_PLACE_L:
        return self.place_l(p1, p2, p3)
    return None


class ACTION:
    MOVE = ACTION_MOVE
    PLACE_I = ACTION_PLACE_I
    PLACE_L = ACTION_PLACE_L
