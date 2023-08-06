from tkinter import ttk


class SelectRemote(ttk.Combobox):
    def __init__(
        self,
        frm: ttk.Frame,
        row: int,
        column: int,
        columnspan: int,
        selection: callable,
    ):
        super().__init__(frm, state="readonly")
        self.set("(Select a remote)")
        self.bind("<<ComboboxSelected>>", selection)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="ew")
