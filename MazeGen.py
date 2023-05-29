from numpy.random import shuffle
import numpy as np


class Kruskal():
    def __init__(self, h, w):
        assert w >= 3 and h >= 3, "Mazes cannot be smaller than 3x3."
        self.h = h
        self.w = w
        self.H = self.h
        self.W = self.w

    def _find_neighbors(self, r, c, grid, is_wall=False):

        ns = []

        if r > 1 and grid[r - 2][c] == is_wall:
            ns.append((r - 2, c))
        if r < self.H - 2 and grid[r + 2][c] == is_wall:
            ns.append((r + 2, c))
        if c > 1 and grid[r][c - 2] == is_wall:
            ns.append((r, c - 2))
        if c < self.W - 2 and grid[r][c + 2] == is_wall:
            ns.append((r, c + 2))

        shuffle(ns)
        return ns

    def generate(self):
        """highest-level method that implements the maze-generating algorithm

        Returns:
            np.array: returned matrix
        """
        # create empty grid
        grid = np.empty((self.H, self.W), dtype=np.int8)
        grid.fill(1)

        forest = []
        for row in range(1, self.H - 1, 2):
            for col in range(1, self.W - 1, 2):
                forest.append([(row, col)])
                grid[row][col] = 0

        edges = []
        for row in range(2, self.H - 1, 2):
            for col in range(1, self.W - 1, 2):
                edges.append((row, col))
        for row in range(1, self.H - 1, 2):
            for col in range(2, self.W - 1, 2):
                edges.append((row, col))

        shuffle(edges)

        while len(forest) > 1:
            ce_row, ce_col = edges[0]
            edges = edges[1:]

            tree1 = -1
            tree2 = -1

            if ce_row % 2 == 0:  # even-numbered row: vertical wall
                tree1 = sum([i if (ce_row - 1, ce_col) in j else 0 for i, j in enumerate(forest)])
                tree2 = sum([i if (ce_row + 1, ce_col) in j else 0 for i, j in enumerate(forest)])
                
            else:  # odd-numbered row: horizontal wall
                tree1 = sum([i if (ce_row, ce_col - 1) in j else 0 for i, j in enumerate(forest)])
                tree2 = sum([i if (ce_row, ce_col + 1) in j else 0 for i, j in enumerate(forest)])

            if tree1 != tree2:
                new_tree = forest[tree1] + forest[tree2]
                temp1 = list(forest[tree1])
                temp2 = list(forest[tree2])
                # faster than forest.remove(temp1)
                forest = [x for x in forest if x != temp1]
                forest = [x for x in forest if x != temp2]
                forest.append(new_tree)
                grid[ce_row][ce_col] = 0

        return grid
