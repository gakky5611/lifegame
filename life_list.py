import random
import copy
from typing import List

class Cell():
    cells: List[List[bool]]

    def __init__(self, w, h, seed=10):
        random.seed()
        probability = seed / 100
        self.w = w
        self.h = h
        self.cells = [[True if random.random() < probability else False for i in range(self.w)] for j in range(self.h)]

    def dead_or_alive(self, x, y):
        if self.cells[y][x]:
            return True
        else:
            return False

    def get_env(self, x, y):
        x_p = [-1, 0, 1]
        y_p = [-1, 0, 1]
        r = 0
        for i in y_p:
            for j in x_p:
                try:
                    if self.cells[y + i][x + j] and (i != 0 or j != 0) and (y + i) >= 0 and (x + j) >= 0:
                        r += 1
                except IndexError:
                    pass
        return r

    def next_gen(self):
        n_cell = copy.copy(self.cells)
        for i in range(self.h):
            for j in range(self.w):
                if self.dead_or_alive(j, i):
                    if self.get_env(j, i) == 2 or self.get_env(j, i) == 3:
                        n_cell[i][j] = True
                    else:
                        n_cell[i][j] = False
                else:
                    if self.get_env(j, i) == 3:
                        n_cell[i][j] = True
                    else:
                        n_cell[i][j] = False

        self.cells = n_cell