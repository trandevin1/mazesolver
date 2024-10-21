from tkinter import Tk, BOTH, Canvas, Menu, Toplevel, Label, Entry, Button, ttk
import re
from maze import Maze, PrintCommand, ChangeConfiguration

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
        row=10,
        column=10,
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
        self.maze.inital_run()

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
        self.root = root
        self.pack(fill=BOTH, expand=1)

        # create menubar widget
        MenuBar(root)

    def clear_screen(self):
        self.delete("all")

    def resize_canvas(self, resolution):
        if not self.root.maze.draw_state:
            self.config(width=resolution[0], height=resolution[1])
            self.clear_screen()

    def draw_line(self, line, fill_color="black"):
        line.draw(self, fill_color)


class MenuBar(Menu):
    def __init__(self, root):
        super().__init__(root)
        self.option = MenuOption(root)
        self.add_cascade(label="Options", menu=self.option)
        root.config(menu=self)


# TODO make a class to contain the maze config window


class MenuOption(Menu):
    def __init__(self, root):
        self.root_win = root
        super().__init__(root, tearoff=0)
        self.add_command(label="Maze Configuration", command=self.maze_configuration)
        self.add_command(label="Exit", command=self.root_win.close)

    def maze_configuration(self):
        # make a window
        config_window = Window(self.root_win, "Maze Configuration", "300x600")
        config_window.resizable(False, False)

        config_window.columnconfigure((0, 1), weight=1, uniform="a")
        config_window.rowconfigure((0, 1, 2, 3, 4, 5, 6, 8, 9), weight=1, uniform="a")

        # create widgets
        row_label = Label(config_window, text="Row:")
        column_label = Label(config_window, text="Column:")
        display_label = Label(config_window, text="Resolution:")
        break_speed_label = Label(config_window, text="Wall Break Speed:")
        cell_speed_label = Label(config_window, text="Cell Draw Speed:")
        path_speed_label = Label(config_window, text="Path Speed:")
        row_label_field = Entry(
            config_window,
            validate="key",
            validatecommand=(config_window.register(self.validate_int_val), "%P"),
        )
        column_label_field = Entry(
            config_window,
            validate="key",
            validatecommand=(config_window.register(self.validate_int_val), "%P"),
        )
        cell_speed_entry = Entry(
            config_window,
            validate="key",
            validatecommand=(config_window.register(self.validate_float_val), "%P"),
        )
        break_speed_entry = Entry(
            config_window,
            validate="key",
            validatecommand=(config_window.register(self.validate_float_val), "%P"),
        )
        path_speed_entry = Entry(
            config_window,
            validate="key",
            validatecommand=(config_window.register(self.validate_float_val), "%P"),
        )

        set_button = Button(
            config_window,
            text="Set",
            command=lambda: self.change_maze_size(row_label_field, column_label_field),
        )
        display_combo = ttk.Combobox(
            config_window,
            values=list(DISPLAY_RESOLUTIONS.keys()),
            width=10,
            state="readonly",
        )
        resize_button = Button(
            config_window,
            text="Resize",
            command=lambda: self.root_win.canvas.resize_canvas(
                DISPLAY_RESOLUTIONS[display_combo.get()]
            ),
        )
        set_speed_button = Button(
            config_window, text="Set Speeds", command=lambda: print("sonic")
        )

        # position the widgets and draw them
        row_label.grid(row=0, column=0, sticky="n")
        row_label_field.grid(row=0, column=0, sticky="s")
        column_label.grid(row=0, column=1, sticky="n")
        column_label_field.grid(row=0, column=1, sticky="s")
        set_button.grid(row=1, column=0, columnspan=2, sticky="")

        display_label.grid(row=2, column=0, sticky="ns")
        resize_button.grid(row=3, column=0, columnspan=2, sticky="n")

        cell_speed_label.grid(row=3, column=0, sticky="s")
        cell_speed_entry.grid(row=3, column=1, sticky="ws")
        break_speed_label.grid(row=4, column=0, sticky="")
        break_speed_entry.grid(row=4, column=1, sticky="w")
        path_speed_label.grid(row=5, column=0, sticky="n")
        path_speed_entry.grid(row=5, column=1, sticky="nw")
        set_speed_button.grid(row=5, column=0, columnspan=2, sticky="s")

        row_label_field.insert(0, "12")
        column_label_field.insert(0, "12")
        cell_speed_entry.insert(0, "0.0")
        break_speed_entry.insert(0, "0.0")
        path_speed_entry.insert(0, "0.0")
        display_combo.grid(row=2, column=1)
        display_combo.current(0)

        # run_button = Button(config_window, text="Run", command=lambda: print("run"))
        # run_button.grid(row=5, column=0, columnspan=2, sticky="s")

    def validate_float_val(self, value):
        if re.match("^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$", value):
            return True
        return False

    def validate_int_val(self, value):
        if (re.match("^[0-9]*$", value)) and (len(value) < 4):
            return True
        return False

    def change_maze_size(self, row, column):
        row_value = row.get()
        column_value = column.get()
        if (
            row_value != ""
            and column_value != ""
            and (2 < int(row_value) < 101)
            and (2 < int(column_value) < 101)
            and not self.root_win.maze.draw_state
        ):
            row.configure(highlightbackground="green", highlightcolor="green")
            column.configure(highlightbackground="green", highlightcolor="green")
            self.root_win.canvas.clear_screen()
            cmd = ChangeConfiguration(self.root_win.maze)
            cmd.execute(int(row_value), int(column_value))
        else:
            row.configure(highlightbackground="red", highlightcolor="red")
            column.configure(highlightbackground="red", highlightcolor="red")


class Window(Toplevel):
    def __init__(self, root, title, geometry):
        super().__init__(root)
        self.title(title)
        self.geometry(geometry)
