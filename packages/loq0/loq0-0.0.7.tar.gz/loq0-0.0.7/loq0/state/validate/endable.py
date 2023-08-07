import numpy as np
from ...const import BOARD_SIZE, I_COUNT, L_COUNT

dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]


def bfs(self, stk, pl):
    visited = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=bool)
    visited[stk[0][0] - 1, stk[0][1] - 1] = True
    while len(stk) > 0:
        x, y = stk.pop()
        for i in range(4):
            if self.movable((x + dx[i], y + dy[i]), (x, y)) and not visited[x + dx[i] - 1, y + dy[i] - 1]:
                if pl == 0 and x + dx[i] == BOARD_SIZE:
                    return True
                elif pl == 1 and y + dy[i] == BOARD_SIZE:
                    return True
                visited[x - 1, y - 1] = True
                stk.append((x + dx[i], y + dy[i]))
    return False


def endable(self):
    return bfs(self, [self.position()], self.player()) and bfs(self, [self.position(True)], self.player(True))
