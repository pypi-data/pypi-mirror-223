from tkinter import ttk, StringVar


class StartupState(ttk.Label):
    def __init__(
        self, frm: ttk.Frame, row: int, column: int, columnspan: int, pady: int
    ):
        self.text = StringVar(frm, "checking ...")
        super().__init__(frm, textvariable=self.text)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="nw", pady=pady)

    def set(self, text: str):
        self.text.set(text)
