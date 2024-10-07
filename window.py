from tkinter import Tk, BOTH, Canvas, Menu, Toplevel, Label, Entry, Button, ttk


DISPLAY_RESOLUTIONS = {
    "1920×1080": (1920, 1080),
    "1366×768": (1366, 768),
    "1680x1050": (1680, 1050),
    "1680x1200": (1680, 1200),
    "1280x1024": (1280, 1024),
    "1280x800": (1280, 800),
    "1280x720": (1280, 720),
    "1024x768": (1024, 768),
    "800x600": (800, 600),
}


class Window:
    def __init__(self, width, height):
        self.root_widget = Tk()
        self.root_widget.title("Main Window")
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
        self.root_widget.option_add("*tearoff", False)
        self.init_menu_bar()
        self.canvas = Canvas(self.root_widget, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False

    def resize_canvas(self, new_width, new_height):
        self.canvas.config(width=new_width, height=new_height)

    def clear_screen(self):
        self.canvas.delete("all")

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

    def init_menu_bar(self):
        menubar = Menu(self.root_widget)
        optionsmenu = Menu(menubar, tearoff=0)
        optionsmenu.add_command(
            label="Maze Configuration", command=self.maze_configuration
        )
        optionsmenu.add_command(label="Exit", command=self.close)
        menubar.add_cascade(label="Options", menu=optionsmenu)
        self.root_widget.config(menu=menubar)

    def maze_configuration(self):
        # create configuration window
        new_window = Toplevel(self.root_widget)
        new_window.title("Maze Configuration")
        new_window.geometry("500x300")

        # create all labels
        row_label = Label(new_window, text="Row")
        column_label = Label(new_window, text="Column")
        display_label = Label(new_window, text="Resolution:")

        row_label.grid(row=0, column=0)
        column_label.grid(row=1, column=0)
        display_label.grid(row=2, column=0)

        # entry fields
        row_label_field = Entry(new_window, width=5)
        column_label_field = Entry(new_window, width=5)
        row_label_field.grid(row=0, column=1)
        column_label_field.grid(row=1, column=1)
        row_label_field.insert(0, 12)
        column_label_field.insert(3, 12)

        display = ttk.Combobox(new_window, )
        set_button = Button(
            new_window,
            text="Set",
            command=lambda: self.get_val(row_label_field, column_label_field),
        )
        set_button.grid(row=0, column=3)

    def get_val(self, row, column):
        # TODO
        row_val = row.get()
        col_val = column.get()

    def validate_val(self):
        # TODO
        pass
