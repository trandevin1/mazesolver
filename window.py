from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.root_widget = Tk()
        self.root_widget.title("Main Window")
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root_widget, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False

    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)

    
