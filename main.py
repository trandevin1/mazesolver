
from window import Window
import point
import cell


def main():
    win = Window(800, 600)

    pt1 = point.Point(200, 500)
    pt2 = point.Point(100, 200)
    line = point.Line(pt1, pt2)

    pt3 = point.Point(100, 100)
    pt4 = point.Point(200, 200)
    line2 = point.Line(pt3, pt4)

    cell1 = cell.Cell(pt3, pt4)

    win.draw_cell(cell1, "black")
    # win.draw_line(line, "red")
    # win.draw_line(line2, "black")

    win.wait_for_close()


if __name__ == "__main__":
    main()
