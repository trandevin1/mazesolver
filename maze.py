from cell import Cell
from time import sleep
import random


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
        seed=None,
        cell_draw_speed=0,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.cell_draw_speed = cell_draw_speed
        self._create_cells()
        random.seed(seed) if seed else None

    def change_configuration(self, row, column):
        pass

    def _create_cells(self):
        self._cells = []
        for row in range(self._num_rows):
            col_list = []
            for col in range(self._num_cols):
                col_list.append(Cell(self._win))
            self._cells.append(col_list)

        self._win.clear_screen()
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
        self._animate(self.cell_draw_speed)

    def _animate(self, time=0.05):
        if not self._win:
            return
        self._win.redraw()
        sleep(time)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cells(0, 0)
        self._cells[self._num_rows - 1][self._num_cols - 1].has_bottom_wall = False
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
            self._animate()

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

        # check right
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

    def _reset_visited(self):
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                if self._cells[i][j]._visited:
                    self._cells[i][j]._visited = False

    def solve(self, method="DFS"):
        if method == "DFS":
            return self._solve_r(0, 0)
        return self._solve_bfs(0, 0)

    def _solve_r(self, i, j):
        self._animate(0.15)
        current_cell = self._cells[i][j]
        current_cell._visited = True

        if current_cell == self._cells[self._num_rows - 1][self._num_cols - 1]:
            return True

        directions = self._check_adjacent_cells(i, j)

        for direction in directions:
            next_cell = self._cells[direction[0]][direction[1]]
            if direction[2] == "up":
                # check that the current cell bottom wall is not there
                if not current_cell.has_bottom_wall and not next_cell.has_top_wall:
                    current_cell.draw_move(next_cell)
                    if self._solve_r(direction[0], direction[1]):
                        return True
                    else:
                        current_cell.draw_move(next_cell, True)

            elif direction[2] == "down":
                # check that the current cell bottom wall is not there
                if not current_cell.has_top_wall and not next_cell.has_bottom_wall:
                    current_cell.draw_move(next_cell)
                    if self._solve_r(direction[0], direction[1]):
                        return True
                    else:
                        current_cell.draw_move(next_cell, True)

            elif direction[2] == "left":
                if not current_cell.has_left_wall and not next_cell.has_right_wall:
                    current_cell.draw_move(next_cell)
                    if self._solve_r(direction[0], direction[1]):
                        return True
                    else:
                        current_cell.draw_move(next_cell, True)
            else:
                if not current_cell.has_right_wall and not next_cell.has_left_wall:
                    current_cell.draw_move(next_cell)
                    if self._solve_r(direction[0], direction[1]):
                        return True
                    else:
                        current_cell.draw_move(next_cell, True)
        return False

    def _solve_bfs(self, i, j):
        to_visit = [(i, j)]

        while len(to_visit) != 0:
            self._animate()
            current_cell = to_visit.pop(0)
            i, j = current_cell[0], current_cell[1]
            current_cell = self._cells[current_cell[0]][current_cell[1]]
            current_cell._visited = True
            if current_cell == self._cells[self._num_rows - 1][self._num_cols - 1]:
                return True

            neighbors = self._check_adjacent_cells(i, j)

            for neighbor in neighbors:
                next_cell = self._cells[neighbor[0]][neighbor[1]]
                direction = neighbor[2]

                if direction == "up":
                    if not current_cell.has_bottom_wall and not next_cell.has_top_wall:
                        current_cell.draw_move(next_cell)
                        to_visit.append(neighbor)

                elif direction == "down":
                    if not current_cell.has_top_wall and not next_cell.has_bottom_wall:
                        current_cell.draw_move(next_cell)
                        to_visit.append(neighbor)

                elif direction == "left":
                    if not current_cell.has_left_wall and not next_cell.has_right_wall:
                        current_cell.draw_move(next_cell)
                        to_visit.append(neighbor)

                else:
                    if not current_cell.has_right_wall and not next_cell.has_left_wall:
                        to_visit.append(neighbor)
                        current_cell.draw_move(next_cell)

        return False
