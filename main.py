from window import Window
from point import Line, Point
from cell import Cell
from maze import Maze


def main():
    width = 1920
    height = 1080
    win = Window(width, height)

    num_rows = 10
    num_cols = 10
    margin = 30

    x_ratio = (width - 2 * margin) // num_rows
    y_ratio = (height - 2 * margin) // num_cols

    maze = Maze(margin, margin, num_rows, num_cols, x_ratio, y_ratio, win, 10)
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)

    win.wait_for_close()


if __name__ == "__main__":
    main()
