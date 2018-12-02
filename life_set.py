import random

import dataclasses








class Cell:

    @dataclasses.dataclass(frozen = True)
    class P:
        x: int
        y: int

    def __init__(self, w, h, seed=10):
        random.seed()
        self.w = w
        self.h = h
        n_seed = int(self.w * self.h * seed / 100)
        self.cells = set()
        for i in range(n_seed):
            p = self.P(random.randint(0, self.w-1), random.randint(0, self.h-1))
            self.cells.add(p)

    def get_env(self, p):
        x_p = [-1, 0, 1]
        y_p = [-1, 0, 1]

        return {self.P(p.x + j, p.y + i) for j in x_p for i in y_p if i != 0 or j != 0}

    def birth(self, p):
        x_p = [-1, 0, 1]
        y_p = [-1, 0, 1]
        for i in y_p:
            for j in x_p:
                if i != 0 or j != 0:
                    if not {self.P(p.x + j, p.y + i)} <= self.cells:
                        num = len(self.get_env(self.P(p.x + j, p.y + i)) & self.cells)
                        if num == 3:
                            self.n_cells.add(self.P(p.x + j, p.y + i))

    def next_gen(self):
        self.n_cells = set()
        for p in self.cells:
            num = len(self.get_env(p) & self.cells)
            if num == 2 or num == 3:
                self.n_cells.add(p)
            self.birth(p)

        self.cells = self.n_cells

