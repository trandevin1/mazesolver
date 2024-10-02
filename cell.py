from point import Line, Point


class Cell:
    def __init__(self, win):
        self._win = win
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self.has_bottom_wall = True
        self.has_top_wall = True
        self.has_left_wall = True
        self.has_right_wall = True

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        
    def draw_move(self, to_cell, undo=False):
        fill_color = "grey"
        if undo:
            fill_color = "red"
        mid = ((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        mid_to_cell = ((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)

        line = Line(Point(mid[0], mid[1]), Point(mid_to_cell[0], mid_to_cell[1]))
        self._win.draw_line(line, fill_color)

