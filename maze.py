from cell import Cell
from time import sleep
import random


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._create_cells()
        random.seed(seed) if seed else None

    def _create_cells(self):

        for row in range(self._num_rows):
            col_list = []
            for col in range(self._num_cols):
                col_list.append(Cell(self._win))
            self._cells.append(col_list)

        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cells(i, j)

    def _draw_cells(self, i, j):
        if not self._win:
            return
        cell = self._cells[i][j]

        top_left_x = self._x1 + (self._cell_size_x * i)
        top_left_y = self._y1 + (self._cell_size_y * j)
        bottom_right_x = top_left_x + self._cell_size_x
        bottom_right_y = top_left_y + self._cell_size_y
        cell.draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        self._animate()

    def _animate(self):
        if not self._win:
            return
        self._win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0].has_top_wall = False
        self._draw_cells(0, 0)
        exit_cell = self._cells[self._num_rows - 1][
            self._num_cols - 1
        ].has_bottom_wall = False
        self._draw_cells(self._num_rows - 1, self._num_cols - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True

        while True:
            to_visit = []

            to_visit.extend(self._check_adjacent_cells(i, j))

            if not to_visit:
                cell = self._cells[i][j]
                self._cells[i][j].draw(cell._x1, cell._y1, cell._x2, cell._y2)
                return

            random_direction = random.choice(to_visit)
            self._break_walls((i, j), random_direction, random_direction[2])
            self._break_walls_r(random_direction[0], random_direction[1])

    def _check_adjacent_cells(self, i, j):
        to_visit = []
        # check above
        if ((j + 1) > -1 and j + 1 < self._num_cols) and (
            self._cells[i][j + 1]._visited == False
        ):
            to_visit.append((i, j + 1, "up"))
        # check below
        if ((j - 1) > -1 and j - 1 < self._num_cols) and (
            self._cells[i][j - 1]._visited == False
        ):
            to_visit.append((i, j - 1, "down"))

        # check left
        if ((i - 1 > -1) and i - 1 < self._num_rows) and (
            self._cells[i - 1][j]._visited == False
        ):
            to_visit.append((i - 1, j, "left"))

        if ((i + 1 > -1) and i + 1 < self._num_rows) and (
            self._cells[i + 1][j]._visited == False
        ):
            to_visit.append((i + 1, j, "right"))

        return to_visit

    def _break_walls(self, current, next, direction):
        if direction == "up":
            self._cells[current[0]][current[1]].has_bottom_wall = False
            self._cells[next[0]][next[1]].has_top_wall = False
        elif direction == "down":
            self._cells[current[0]][current[1]].has_top_wall = False
            self._cells[next[0]][next[1]].has_bottom_wall = False
        elif direction == "left":
            self._cells[current[0]][current[1]].has_left_wall = False
            self._cells[next[0]][next[1]].has_right_wall = False
        elif direction == "right":
            self._cells[current[0]][current[1]].has_right_wall = False
            self._cells[next[0]][next[1]].has_left_wall = False
        else:
            return
