
class Point:
    """
    Object to define a point in the GUI coordinate plane
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    """
    Object to define and draw a line between two points
    """
    def __init__(self, pt1, pt2):
        self.pt1 = pt1
        self.pt2 = pt2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.pt1.x, self.pt1.y, self.pt2.x, self.pt2.y, fill=fill_color, width=2)