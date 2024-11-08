from cell import Cell
from time import sleep, time
import random
from abc import ABC, abstractmethod
from enum import Enum


class SolveMethod(Enum):
    DFS = 0
    BFS = 1
    ASTAR = 2


class Command(ABC):
    """
    Abstract class for command pattern
    """
    def __init__(self, reciever):
        self.reciever = reciever

    @abstractmethod
    def execute(self):
        pass


class ChangeConfiguration(Command):
    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self, row, column):
        self.reciever.draw_state = True
        self.reciever._change_maze_size(row, column)
        self.reciever.draw_state = False


class ChangeAnimationSpeed(Command):
    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self, speed):
        self.reciever.set_animation_draw_speed(speed)


class Run(Command):
    def __init__(self, reciever):
        self.reciever = reciever

    def execute(self, solve_method, row_value, col_value):
        self.reciever.run(solve_method, row_value, col_value)


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
        animation_draw_speed=0.05,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.animation_draw_speed = animation_draw_speed
        self.draw_state = False
        random.seed(seed) if seed else None

    def set_animation_draw_speed(self, speed: float | None = None) -> None:
        if speed is not None:
            self.animation_draw_speed = speed

    def get_animation_draw_speed(self) -> float:
        return self.animation_draw_speed

    def run(self, solve_method, row_value, col_value):
        # TODO
        self.draw_state = True
        self._change_maze_size(row_value, col_value)
        self._create_cells()
        self._break_entrance_and_exit()
        (
            self._break_walls_iteratively(0, 0)
            if self._num_rows > 30 and self._num_cols > 30
            else self._break_walls_r(0, 0)
        )
        self._reset_visited()
        self.solve(solve_method)
        self.draw_state = False

    def inital_run(self):
        self.draw_state = True
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_iteratively(0, 0)
        self._reset_visited()
        self.solve()
        self.draw_state = False

    def _change_maze_size(self, row, column):
        """
        Changes the size of the maze and dimensions of the maze
        """
        if row is not None:
            self._num_rows = row
        if column is not None:
            self._num_cols = column
        self._cell_size_x = (
            self._win.canvas.winfo_width() - 2 * self._x1
        ) // self._num_rows
        self._cell_size_y = (
            self._win.canvas.winfo_height() - 2 * self._y1
        ) // self._num_cols

    def _create_cells(self):
        """
        Create maze cells
        """
        self._cells = []
        for _ in range(self._num_rows):
            col_list = []
            for _ in range(self._num_cols):
                col_list.append(Cell(self._win))
            self._cells.append(col_list)

        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        """
        Draws each cell to the canvas.
        """
        if not self._win:
            return

        # Get current cell to draw
        cell = self._cells[i][j]

        # Calculate position of cell from the canvas
        top_left_x = self._x1 + (self._cell_size_x * i)
        top_left_y = self._y1 + (self._cell_size_y * j)
        bottom_right_x = top_left_x + self._cell_size_x
        bottom_right_y = top_left_y + self._cell_size_y

        # Draw cell to canvas
        cell.draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        self._animate(self.animation_draw_speed)

    def _animate(self, time=0.05):
        """
        Slows down the drawing animation
        """
        if not self._win:
            return
        self._win.redraw()
        sleep(time)

    def _break_entrance_and_exit(self):
        """
        Set the start and end goal by breaking down the walls.
        """
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_rows - 1][self._num_cols - 1].has_bottom_wall = False
        self._draw_cell(self._num_rows - 1, self._num_cols - 1)

    def _break_walls_r(self, i, j):
        """
        Randomly break down walls between two cells.
        """
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
            self._animate(self.animation_draw_speed)

    def _break_walls_iteratively(self, i, j):
        """
        Breaks down the walls using iteration instead of recursion if the maze is too big.
        """
        to_visit = [(i, j)]

        while to_visit:
            # get current cell
            current = to_visit.pop(-1)
            current_cell = self._cells[current[0]][current[1]]
            current_cell._visited = True

            # get neighbors
            neighbors = self._check_adjacent_cells(current[0], current[1])

            # choose random direction
            if neighbors:
                random_direction = random.choice(neighbors)
                self._break_walls(
                    current,
                    (random_direction[0], random_direction[1]),
                    random_direction[2],
                )
                # draw current cell
                current_cell.draw(
                    current_cell._x1,
                    current_cell._y1,
                    current_cell._x2,
                    current_cell._y2,
                )

                to_visit.extend(neighbors)
                self._animate(self.animation_draw_speed)

    def _check_adjacent_cells(self, i, j):
        """
        Checks adjacent nodes from the given cell index.
        """
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
        """
        Breaks the walls from the current cell and next cell depending on the direction.
        """
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
        """
        This sets all the cells back to unvisited.
        """
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                if self._cells[i][j]._visited:
                    self._cells[i][j]._visited = False

    def solve(self, solve_method=SolveMethod.DFS.value):
        match solve_method:
            case SolveMethod.DFS.value:
                start = time()
                self._solve_r(0, 0)
                end = time()
                algorithm = "Depth First Search"
            case SolveMethod.BFS.value:
                start = time()
                self._solve_bfs(0, 0)
                end = time()
                algorithm = "Breadth First Search"
            case SolveMethod.ASTAR.value:
                start = time()
                self._solve_astar(0, 0)
                end = time()
                algorithm = "A*"
        print(f"{algorithm} time: {end - start} seconds")

    def _solve_r(self, i, j):
        """
        Simple Depth First Search pathing using recursion and backtracking.
        """
        self._animate(self.animation_draw_speed)

        current_cell = self._cells[i][j]
        current_cell._visited = True

        if current_cell == self._cells[self._num_rows - 1][self._num_cols - 1]:
            return True

        directions = self._check_adjacent_cells(i, j)

        # TODO make this look nicer lol
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
        """
        Simple breadth first search pathing
        """

        # Instantiate start node and node queue
        start = (i, j)
        to_visit = [start]

        came_from = {}

        # Get current node until queue is empty
        while len(to_visit) != 0:
            self._animate(self.animation_draw_speed)
            current_cell = to_visit.pop(0)
            i, j = current_cell[0], current_cell[1]
            current_cell = self._cells[i][j]
            current_cell._visited = True

            # Found Goal Cell
            if current_cell == self._cells[self._num_rows - 1][self._num_cols - 1]:

                # TODO just make this into another function too much for this
                # Backtrack to get the path the algorithm took
                path = []
                traversal = (i, j)
                while traversal in came_from:
                    path.append(traversal)
                    traversal = came_from[traversal]
                path.append(start)
                path.reverse()

                # Highlights the path from start to finish
                for index in range(len(path) - 1):
                    current = path[index]
                    next = path[index + 1]
                    current_node = self._cells[current[0]][current[1]]
                    next_node = self._cells[next[0]][next[1]]
                    current_node.draw_move(next_node, True)

                return True

            # Get next valid cell to move
            neighbors = self._check_adjacent_cells(i, j)

            for neighbor in neighbors:
                # Find next cell to move
                next_cell = self._cells[neighbor[0]][neighbor[1]]
                direction = neighbor[2]

                # TODO possibly make this into another function for readability
                if direction == "up":
                    if not current_cell.has_bottom_wall and not next_cell.has_top_wall:
                        current_cell.draw_move(next_cell)
                        to_visit.append(neighbor)
                        came_from[(neighbor[0], neighbor[1])] = (i, j)

                elif direction == "down":
                    if not current_cell.has_top_wall and not next_cell.has_bottom_wall:
                        current_cell.draw_move(next_cell)
                        to_visit.append(neighbor)
                        came_from[(neighbor[0], neighbor[1])] = (i, j)

                elif direction == "left":
                    if not current_cell.has_left_wall and not next_cell.has_right_wall:
                        current_cell.draw_move(next_cell)
                        to_visit.append(neighbor)
                        came_from[(neighbor[0], neighbor[1])] = (i, j)

                else:
                    if not current_cell.has_right_wall and not next_cell.has_left_wall:
                        to_visit.append(neighbor)
                        current_cell.draw_move(next_cell)
                        came_from[(neighbor[0], neighbor[1])] = (i, j)

        return False

    def _solve_astar(self, i, j):
        """
        A simplified version of the A* algorithm using a basic heuristic to find the finish line.
        """

        # Instantiate start position and node queue
        start = (0, (i, j))
        open_set = [start]
        came_from = {}
        g_score = {start[1]: 0}

        # While there are nodes to visit
        while open_set:
            # Draw the move from one cell to another
            self._animate(self.animation_draw_speed)

            # Get current node
            f_score, current = open_set.pop(0)
            current_cell = self._cells[current[0]][current[1]]
            current_cell.visited = True

            # End goal would be the last cell
            if current == (self._num_rows - 1, self._num_cols - 1):
                return True

            neighbors = self._check_adjacent_cells(current[0], current[1])

            for neighbor in neighbors:
                next_cell = self._cells[neighbor[0]][neighbor[1]]
                direction = neighbor[2]
                tentative_g = g_score[current] + 1

                if (neighbor[0], neighbor[1]) not in g_score or tentative_g < g_score[
                    (neighbor[0], neighbor[1])
                ]:
                    if direction == "up":
                        if (
                            not current_cell.has_bottom_wall
                            and not next_cell.has_top_wall
                        ):
                            g_score[(neighbor[0], neighbor[1])] = tentative_g
                            f_score = tentative_g + self._astar_heuristic(
                                (neighbor[0], neighbor[1])
                            )
                            open_set.append((f_score, (neighbor[0], neighbor[1])))
                            current_cell.draw_move(next_cell)
                            came_from[(neighbor[0], neighbor[1])] = current

                    elif direction == "down":
                        if (
                            not current_cell.has_top_wall
                            and not next_cell.has_bottom_wall
                        ):
                            g_score[(neighbor[0], neighbor[1])] = tentative_g
                            f_score = tentative_g + self._astar_heuristic(
                                (neighbor[0], neighbor[1])
                            )
                            open_set.append((f_score, (neighbor[0], neighbor[1])))
                            current_cell.draw_move(next_cell)

                            came_from[(neighbor[0], neighbor[1])] = current

                    elif direction == "left":
                        if (
                            not current_cell.has_left_wall
                            and not next_cell.has_right_wall
                        ):
                            g_score[(neighbor[0], neighbor[1])] = tentative_g
                            f_score = tentative_g + self._astar_heuristic(
                                (neighbor[0], neighbor[1])
                            )
                            open_set.append((f_score, (neighbor[0], neighbor[1])))
                            current_cell.draw_move(next_cell)

                            came_from[(neighbor[0], neighbor[1])] = current
                    else:
                        if (
                            not current_cell.has_right_wall
                            and not next_cell.has_left_wall
                        ):
                            g_score[(neighbor[0], neighbor[1])] = tentative_g
                            f_score = tentative_g + self._astar_heuristic(
                                (neighbor[0], neighbor[1])
                            )
                            open_set.append((f_score, (neighbor[0], neighbor[1])))
                            current_cell.draw_move(next_cell)

                            came_from[(neighbor[0], neighbor[1])] = current

        return False

    def _astar_heuristic(self, start):
        """
        Using the Manhattan Distance Formula as the heuristic
        """
        return abs(start[0] - (self._num_rows - 1)) + abs(
            start[1] - (self._num_cols - 2)
        )
