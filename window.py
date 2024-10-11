from tkinter import Tk, BOTH, Canvas, Menu, Toplevel, Label, Entry, Button, ttk
import re
from maze import Maze, PrintCommand

DISPLAY_RESOLUTIONS = {
    "1920×1080": (1920, 1080),
    "1680x1050": (1680, 1050),
    "1680x1200": (1680, 1200),
    "1366×768": (1366, 768),
    "1280x1024": (1280, 1024),
    "1280x800": (1280, 800),
    "1280x720": (1280, 720),
    "1024x768": (1024, 768),
    "800x600": (800, 600),
}


class App(Tk):
    def __init__(
        self,
        width=800,
        height=600,
        x_margin=30,
        y_margin=30,
        row=9,
        column=9,
    ):
        """
        This is the main app where all the GUI is initialized along with
        the maze.
        """
        super().__init__()
        self.title("Maze Solver")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.option_add("*tearoff", False)
        self.minsize(600, 600)
        self.running = False

        # create widgets
        self.canvas = CustomCanvas(self, width, height)

        # create maze
        self.maze = Maze(
            x_margin,
            y_margin,
            row,
            column,
            (width - 2 * x_margin) // row,
            (height - 2 * y_margin) // column,
            self,
            None,
        )
        self.maze.run()

        # main loop
        self.wait_for_close()

    def close(self):
        print("closing")
        self.running = False

    def redraw(self):
        self.update_idletasks()
        self.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()


class CustomCanvas(Canvas):
    def __init__(self, root, width, height):
        super().__init__(root, bg="white", width=width, height=height)
        self.pack(fill=BOTH, expand=1)

        # create menubar widget
        MenuBar(root)

    def clear_screen(self):
        self.delete("all")

    def resize_canvas(self, resolution):
        self.config(width=resolution[0], height=resolution[1])
        self.clear_screen()

    def draw_line(self, line, fill_color="black"):
        line.draw(self, fill_color)


class MenuBar(Menu):
    def __init__(self, root):
        super().__init__(root)
        option = MenuOption(root)
        self.add_cascade(label="Options", menu=option)
        root.config(menu=self)


class MenuOption(Menu):
    def __init__(self, root):
        self.root_win = root
        super().__init__(root, tearoff=0)
        self.add_command(label="Maze Configuration", command=self.maze_configuration)
        self.add_command(label="Exit", command=root.close)

    def maze_configuration(self):
        # make a window
        config_window = Window(self.root_win, "Maze Configuration", "800x600")
        config_window.grid()

        # create all labels
        row_label = Label(config_window, text="Row:")
        column_label = Label(config_window, text="Column:")
        display_label = Label(config_window, text="Resolution:")

        # position the labels
        row_label.grid(row=0, column=0, sticky="w")
        column_label.grid(row=1, column=0, sticky="w")
        display_label.grid(row=2, column=0)

        # entry fields
        row_label_field = Entry(
            config_window,
            width=5,
            validate="key",
            validatecommand=(config_window.register(self.validate_int_val), "%S"),
        )
        column_label_field = Entry(
            config_window,
            width=5,
            validate="key",
            validatecommand=(config_window.register(self.validate_int_val), "%S"),
        )
        row_label_field.grid(row=0, column=1, sticky="w")
        column_label_field.grid(row=1, column=1, sticky="w")
        row_label_field.insert(0, 12)
        column_label_field.insert(3, 12)

        display_combo = ttk.Combobox(
            config_window,
            values=list(DISPLAY_RESOLUTIONS.keys()),
            width=10,
            state="readonly",
        )

        display_combo.grid(row=2, column=1)
        display_combo.current(0)

        set_button = Button(
            config_window,
            text="Set",
            command=lambda: self.send_values(
                row_label_field.get(), column_label_field.get()
            ),
        )
        set_button.grid(row=0, column=1, sticky="e")

        resize_button = Button(
            config_window,
            text="Resize",
            command=lambda: self.root_win.canvas.resize_canvas(
                DISPLAY_RESOLUTIONS[display_combo.get()]
            ),
        )
        resize_button.grid(row=2, column=2)

    def validate_int_val(self, value):
        if not re.match("^[0-9]*$", value):
            return False
        return True

    def change_maze_config(self, row, column):
        # TODO

        if not self.root_win.maze:
            print("no maze")

        print(row, column)
        self.root_win.maze.change_configuration(int(row), int(column))

    def send_values(self, row, column):
        cmd = PrintCommand(self.root_win.maze)
        cmd.execute(values=(row, column))


class Window(Toplevel):
    def __init__(self, root, title, geometry):
        super().__init__(root)
        self.title(title)
        self.geometry(geometry)
