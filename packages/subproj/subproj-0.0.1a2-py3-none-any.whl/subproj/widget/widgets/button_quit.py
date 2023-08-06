from tkinter import ttk


class ButtonQuit(ttk.Button):
    def __init__(
        self,
        frm: ttk.Frame,
        row: int,
        column: int,
        columnspan: int,
        pady: int,
        quit: callable,
    ):
        super().__init__(frm, text="Quit", command=quit)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="w", pady=pady)
