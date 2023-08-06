from tkinter import ttk


class SelectSubProj(ttk.Combobox):
    def __init__(
        self, frm: ttk.Frame, row: int, column: int, columnspan: int, refresh: callable
    ):
        super().__init__(frm, values=["Refresh"], state="readonly")
        self.grid(row=row, column=column, columnspan=columnspan, sticky="ew")

        def _refresh(event):
            self.set("")
            refresh()

        self.bind("<<ComboboxSelected>>", _refresh)
