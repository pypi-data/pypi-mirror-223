from tkinter import ttk


class Label(ttk.Label):
    def __init__(
        self,
        frm: ttk.Frame,
        row: int,
        column: int,
        columnspan: int,
        pady: int,
        text: str,
    ):
        super().__init__(frm, text=text)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="nw", pady=pady)
