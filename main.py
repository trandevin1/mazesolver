from window import Window
from point import Line, Point
from cell import Cell
from maze import Maze


def main():
    win = Window(1920, 1080)
    num_rows = 7
    num_cols = 7
    x_ratio = 1920 // num_rows - 10
    y_ratio = 1080 // num_cols - 10

    maze = Maze(10, 10, num_rows, num_cols, x_ratio, y_ratio, win)
    maze._break_entrance_and_exit()

    win.wait_for_close()


if __name__ == "__main__":
    main()
