import unittest
from maze import Maze


class MazeTest(unittest.TestCase):
    def test_maze_create_cells_1(self):
        num_cols = 12
        num_rows = 10

        maze = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(len(maze._cells), maze._num_rows)
        self.assertEqual(len(maze._cells[0]), maze._num_cols)

    def test_maze_create_cells_2(self):
        num_cols = num_rows = 5
        start_pos = 100

        maze = Maze(start_pos, start_pos, num_rows, num_cols, 10, 10)

        self.assertEqual(len(maze._cells), maze._num_rows)
        self.assertEqual(len(maze._cells[0]), maze._num_rows)

    def test_maze_create_cells_3(self):
        num_cols = 100
        num_rows = 1000

        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(maze._cells), maze._num_rows)
        self.assertEqual(len(maze._cells[0]), num_cols)

    def test_maze_break_entrance_and_exit(self):
        num_cols = 100
        num_rows = 1000

        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        maze._break_entrance_and_exit()

        self.assertEqual(maze._cells[0][0].has_top_wall, False)
        self.assertEqual(maze._cells[num_rows - 1][num_cols - 1].has_bottom_wall, False)


if __name__ == "__main__":
    unittest.main()
