from window import Window
from maze import Maze
import time


def main():
    width = 1920
    height = 1080
    win = Window(width, height)

    num_rows = 16
    num_cols = 16
    margin = 30

    x_ratio = (width - 2 * margin) // num_rows
    y_ratio = (height - 2 * margin) // num_cols

    maze = Maze(
        margin,
        margin,
        num_rows,
        num_cols,
        x_ratio,
        y_ratio,
        win,
    )
    # need to create a function to reset these vars
    maze._num_cols = 12
    maze._num_rows = 12
    maze._cell_size_x = (width - 2 * margin) // 12
    maze._cell_size_y = (height - 2 * margin) // 12
    maze._create_cells()
    # maze._break_entrance_and_exit()
    # maze._break_walls_r(0, 0)
    # maze._reset_visited()

    # if maze.solve("BFS"):
    #     print("MAZE SOLVED!!!!!")
    # else:
    #     print("NO SOLUTION!!!!!")

    win.wait_for_close()


if __name__ == "__main__":
    main()
