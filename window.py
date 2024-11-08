from tkinter import (
    Tk,
    BOTH,
    Canvas,
    Menu,
    Toplevel,
    Label,
    Entry,
    Button,
    ttk,
    Radiobutton,
    IntVar,
)
import re
from maze import (
    Maze,
    ChangeAnimationSpeed,
    SolveMethod,
    Run,
)

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


class MenuOption(Menu):
    def __init__(self, root):
        self.root_win = root
        super().__init__(root, tearoff=0)
        self.config_window = None
        self.add_command(label="Maze Configuration", command=self.maze_configuration)
        self.add_command(label="Exit", command=self.root_win.close)

    def close_window(self):
        self.config_window.destroy()
        self.config_window = None

    def maze_configuration(self):
        if self.config_window:
            return

        # make a window
        if self.config_window is None:
            self.config_window = MazeConfig(
                self.root_win, "Maze Configuration", "300x400"
            )
            self.config_window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.config_window.resizable(False, False)


class MazeConfig(Toplevel):
    def __init__(self, root, title, geometry):
        super().__init__(root)
        self.root = root
        self.title(title)
        self.geometry(geometry)
        # create rowcol frame
        self.row_col_frame = RowColFrame(self)
        # create display resolution frame
        self.display_resolution_frame = DisplayResolutionFrame(self, self.root)
        # create animation speed frame
        self.animation_speed_frame = AnimationSpeedFrame(self, self.root)
        # create algorithm frame
        self.algorithm_frame = AlgorithmFrame(self, self.root)
        # position the widgets within the window and display them
        self.widget_configuration()

    def widget_configuration(self):
        self.row_col_frame.pack(pady=20)
        self.display_resolution_frame.pack(pady=20)
        self.animation_speed_frame.pack(pady=20)
        self.algorithm_frame.pack(pady=20)


class RowColFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.row_label = Label(self, text="Row:")
        self.column_label = Label(self, text="Column:")
        self.row_label_field = Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_int_val), "%P"),
            width=5,
        )
        self.column_label_field = Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.validate_int_val), "%P"),
            width=5,
        )
        self.position()
        self.row_label_field.insert(0, "12")
        self.column_label_field.insert(0, "12")

    def position(self):
        self.row_label.grid(row=0, column=0)
        self.row_label_field.grid(row=0, column=1)
        self.column_label.grid(row=1, column=0)
        self.column_label_field.grid(row=1, column=1)

    def validate_int_val(self, value):
        if (re.match("^[0-9]*$", value)) and (len(value) < 4):
            return True
        return False

    def get_row_value(self):
        try:
            value = int(self.row_label_field.get())
        except:
            print("something went wrong in converting row value into int")
            value = 12
        return value

    def get_col_value(self):
        try:
            value = int(self.column_label_field.get())
        except:
            print("something went wrong in converting col value into int")
            value = 12
        return value


class DisplayResolutionFrame(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.parent = parent
        self.display_label = Label(self, text="Resolution:")
        self.display_combo = ttk.Combobox(
            self,
            values=list(DISPLAY_RESOLUTIONS.keys()),
            width=10,
            state="readonly",
        )
        self.resize_button = Button(
            self,
            text="Resize",
            command=lambda: root.canvas.resize_canvas(
                DISPLAY_RESOLUTIONS[self.display_combo.get()]
            ),
        )
        self.position()
        self.display_combo.current(0)

    def position(self):
        self.display_label.grid(row=0, column=0)
        self.display_combo.grid(row=0, column=1)
        self.resize_button.grid(row=1, column=0, columnspan=2)


class AnimationSpeedFrame(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.root = root
        self.animation_speed_label = Label(self, text="Cell Draw Speed:")
        self.speed_combo = ttk.Combobox(
            self,
            values=["Very Slow", "Slow", "Normal", "Fast", "Very Fast"],
            width=10,
            state="readonly",
        )
        self.speed_combo.bind("<<ComboboxSelected>>", self.changeAnimationSpeed)
        self.position()
        self.speed_combo.current(2)

    def position(self):
        self.animation_speed_label.grid(row=0, column=0)
        self.speed_combo.grid(row=0, column=1)

    ## TODO
    def changeAnimationSpeed(self, _):
        # speed placeholder for now
        speed = 0.05
        match self.speed_combo.get():
            case "Very Slow":
                speed = 0.3
            case "Slow":
                speed = 0.1
            case "Normal":
                speed = 0.05
            case "Fast":
                speed = 0.005
            case "Very Fast":
                speed = 0.0001
        cmd = ChangeAnimationSpeed(self.root.maze)
        cmd.execute(speed=speed)


class AlgorithmFrame(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        self.parent = parent
        self.root = root
        res = IntVar(self, SolveMethod.DFS.value)

        # get rid of row col set button
        self.ASTAR_radio = Radiobutton(
            self,
            text="A* Pathing",
            variable=res,
            value=SolveMethod.ASTAR.value,
        )
        self.DFS_radio = Radiobutton(
            self,
            text="Depth First Pathing",
            variable=res,
            value=SolveMethod.DFS.value,
        )
        self.BFS_radio = Radiobutton(
            self,
            text="Breadth First Pathing",
            variable=res,
            value=SolveMethod.BFS.value,
        )
        # change placeholder arugments back after refactoring
        self.run_button = Button(
            self,
            text="Run",
            command=lambda: self.runMazeSolver(
                res.get(),
                self.parent.row_col_frame.get_row_value(),
                self.parent.row_col_frame.get_col_value(),
            ),
        )
        self.position()

    def position(self):
        self.ASTAR_radio.grid()
        self.BFS_radio.grid()
        self.DFS_radio.grid()
        self.run_button.grid()

    def runMazeSolver(self, solve_method, row_value=None, column_value=None):
        self.root.canvas.clear_screen()
        match solve_method:
            case SolveMethod.DFS.value:
                self.root.title("Depth First Search")
            case SolveMethod.BFS.value:
                self.root.title("Breadth First Search")
            case SolveMethod.ASTAR.value:
                self.root.title("A* Pathing")
        cmd = Run(self.root.maze)
        cmd.execute(solve_method, row_value=row_value, col_value=column_value)
