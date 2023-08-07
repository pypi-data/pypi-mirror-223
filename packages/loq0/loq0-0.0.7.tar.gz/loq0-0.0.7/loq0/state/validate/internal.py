def block_internal(self, t, x, y, w):
    if t == 1:
        if w == 1:
            if 5 <= x <= 6 and 3 <= y <= 6: return True
        else:
            if 3 <= x <= 6 and 5 <= y <= 6: return True
    elif t == 2:
        if w == 1:
            if x == 4 and y == 4: return False
            if 4 <= x <= 6 and 4 <= y <= 6: return True
        elif w == 2:
            if x == 4 and y == 6: return False
            if 4 <= x <= 6 and 4 <= y <= 6: return True
        elif w == 3:
            if x == 6 and y == 6: return False
            if 4 <= x <= 6 and 4 <= y <= 6: return True
        else:
            if x == 6 and y == 4: return False
            if 4 <= x <= 6 and 4 <= y <= 6: return True

    return False
