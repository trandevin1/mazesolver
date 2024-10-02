from cell import Cell
from time import sleep


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
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
