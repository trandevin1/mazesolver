class Cell:
    def __init__(self, top_left_pt, bottom_right_pt):
        self._x1 = top_left_pt.x
        self._y1 = top_left_pt.y
        self._x2 = bottom_right_pt.x
        self._y2 = bottom_right_pt.y
        self.has_bottom_wall = True
        self.has_top_wall = True
        self.has_left_wall = True
        self.has_right_wall = True

    def draw(self, canvas, fill_color):
        if self.has_left_wall:
            canvas.create_line(
                self._x1,
                self._x1,
                self._x1,
                self._y2,
                fill=fill_color,
                width=2,
            )

        if self.has_right_wall:
            canvas.create_line(
                self._x2,
                self._y2,
                self._x2,
                self._y1,
                fill=fill_color,
                width=2,
            )

        if self.has_bottom_wall:
            canvas.create_line(
                self._x1,
                self._y2,
                self._x2,
                self._y2,
                fill=fill_color,
                width=2,
            )

        if self.has_top_wall:
            canvas.create_line(
                self._x1,
                self._y1,
                self._x2,
                self._y1,
                fill=fill_color,
                width=2,
            )
