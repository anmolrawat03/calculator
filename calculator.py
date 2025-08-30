import tkinter as tk
import re

class Calculator:
    # Centralized styling for easier theme management
    STYLE = {
        'BACKGROUND': '#2E2E2E',
        'DISPLAY_FG': 'white',
        'ENTRY_FG': '#CCCCCC',
        'BTN_BG': '#4A4A4A',
        'BTN_FG': 'white',
        'BTN_ACTIVE_BG': '#6A6A6A',
        'OPERATOR_BTN_BG': '#D35400',
        'OPERATOR_BTN_ACTIVE_BG': '#E67E22',
        'EQUALS_BTN_BG': '#27AE60',
        'EQUALS_BTN_ACTIVE_BG': '#2ECC71',
        'CLOSE_BTN_BG': '#C0392B',
        'CLOSE_BTN_ACTIVE_BG': '#E74C3C',
        'LARGE_FONT': ('Helvetica', 36, 'bold'),
        'SMALL_FONT': ('Helvetica', 14, 'bold'),
    }

    def __init__(self, master):
        self.master = master
        self.calc_expression = ""
        self.drag_x = 0
        self.drag_y = 0

        # Window setup
        master.geometry("320x480+400+200")
        master.overrideredirect(True)
        master.attributes('-alpha', 0.9)
        master.config(bg=self.STYLE['BACKGROUND'])

        # UI Frames
        self.display_frame = tk.Frame(master, bg=self.STYLE['BACKGROUND'])
        self.display_frame.pack(expand=True, fill="both")

        self.buttons_frame = tk.Frame(master, bg=self.STYLE['BACKGROUND'])
        self.buttons_frame.pack(expand=True, fill="both")

        # Create widgets
        self.result_label, self.entry_label = self._setup_display()
        self._setup_buttons()

        # Bindings for window dragging and keyboard input
        master.bind("<Button-1>", self.start_move)
        master.bind("<ButtonRelease-1>", self.stop_move)
        master.bind("<B1-Motion>", self.do_move)
        master.bind("<Key>", self.handle_keypress)

    def _setup_display(self):
        result_label = tk.Label(self.display_frame, text="", anchor=tk.E, bg=self.STYLE['BACKGROUND'],
                               fg=self.STYLE['DISPLAY_FG'], padx=24, font=self.STYLE['LARGE_FONT'])
        result_label.pack(expand=True, fill='both')

        entry_label = tk.Label(self.display_frame, text="", anchor=tk.E, bg=self.STYLE['BACKGROUND'],
                                 fg=self.STYLE['ENTRY_FG'], padx=24, font=self.STYLE['SMALL_FONT'])
        entry_label.pack(expand=True, fill='both')
        return result_label, entry_label

    def _setup_buttons(self):
        buttons = {
            '7': (1, 0), '8': (1, 1), '9': (1, 2), '/': (1, 3),
            '4': (2, 0), '5': (2, 1), '6': (2, 2), '*': (2, 3),
            '1': (3, 0), '2': (3, 1), '3': (3, 2), '-': (3, 3),
            '0': (4, 1), '.': (4, 2), '+': (4, 3)
        }

        for i in range(5): self.buttons_frame.rowconfigure(i, weight=1)
        for i in range(4): self.buttons_frame.columnconfigure(i, weight=1)

        for text, grid_pos in buttons.items():
            button = tk.Button(self.buttons_frame, text=text, font=self.STYLE['SMALL_FONT'],
                               bg=self.STYLE['BTN_BG'], fg=self.STYLE['BTN_FG'], borderwidth=0,
                               activebackground=self.STYLE['BTN_ACTIVE_BG'],
                               command=lambda t=text: self.add_to_expression(t))
            button.grid(row=grid_pos[0], column=grid_pos[1], sticky='nsew', padx=1, pady=1)

        # Special buttons
        tk.Button(self.buttons_frame, text='C', font=self.STYLE['SMALL_FONT'],
                  bg=self.STYLE['OPERATOR_BTN_BG'], fg=self.STYLE['BTN_FG'], borderwidth=0,
                  activebackground=self.STYLE['OPERATOR_BTN_ACTIVE_BG'], command=self.clear).grid(
                      row=0, column=0, columnspan=2, sticky='nsew', padx=1, pady=1)

        tk.Button(self.buttons_frame, text='=', font=self.STYLE['SMALL_FONT'],
                  bg=self.STYLE['EQUALS_BTN_BG'], fg=self.STYLE['BTN_FG'], borderwidth=0,
                  activebackground=self.STYLE['EQUALS_BTN_ACTIVE_BG'], command=self.evaluate).grid(
                      row=4, column=0, sticky='nsew', padx=1, pady=1)

        tk.Button(self.buttons_frame, text='X', font=self.STYLE['SMALL_FONT'],
                  bg=self.STYLE['CLOSE_BTN_BG'], fg=self.STYLE['BTN_FG'], borderwidth=0,
                  activebackground=self.STYLE['CLOSE_BTN_ACTIVE_BG'], command=self.master.quit).grid(
                      row=0, column=2, columnspan=2, sticky='nsew', padx=1, pady=1)

    def add_to_expression(self, value):
        self.calc_expression += str(value)
        self.entry_label.config(text=self.calc_expression)

    def clear(self):
        self.calc_expression = ""
        self.entry_label.config(text="")
        self.result_label.config(text="")

    def evaluate(self):
        # Sanitize the expression to only allow safe characters
        safe_expression = re.sub(r'[^0-9\.\+\-\*\/]', '', self.calc_expression)
        if not safe_expression:
            return

        try:
            result = str(eval(safe_expression))
            self.result_label.config(text=result)
            self.calc_expression = result
        except ZeroDivisionError:
            self.result_label.config(text="Math Error")
            self.calc_expression = ""
        except (SyntaxError, NameError):
            self.result_label.config(text="Syntax Error")
            self.calc_expression = ""

    def handle_keypress(self, event):
        """Handles keyboard input."""
        if event.keysym in "0123456789.+-*/":
            self.add_to_expression(event.keysym)
        elif event.keysym == "Return" or event.char == '=':
            self.evaluate()
        elif event.keysym == "Escape" or event.char.lower() == 'c':
            self.clear()

    # Draggable window methods
    def start_move(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def stop_move(self, event):
        self.drag_x = 0
        self.drag_y = 0

    def do_move(self, event):
        dx = event.x - self.drag_x
        dy = event.y - self.drag_y
        x = self.master.winfo_x() + dx
        y = self.master.winfo_y() + dy
        self.master.geometry(f"+{x}+{y}")

# Main execution block
if __name__ == "__main__":
    app = tk.Tk()
    Calculator(app)
    app.mainloop()
