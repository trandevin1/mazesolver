from window import Window, App
from maze import Maze
import time


def main():
    width = 1920
    height = 1080
    App(width, height)
    # win = Window(width, height)

    # num_rows = 16
    # num_cols = 16
    # margin = 30

    # x_ratio = (width - 2 * margin) // num_rows
    # y_ratio = (height - 2 * margin) // num_cols

    # maze = Maze(
    #     margin,
    #     margin,
    #     num_rows,
    #     num_cols,
    #     x_ratio,
    #     y_ratio,
    #     win,
    # )

    # maze.run()

    # if maze.solve("BFS"):
    #     print("MAZE SOLVED!!!!!")
    # else:
    #     print("NO SOLUTION!!!!!")

    #win.wait_for_close()


if __name__ == "__main__":
    main()
