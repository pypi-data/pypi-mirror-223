from tkinter import ttk


class SelectProj(ttk.Combobox):
    def __init__(
        self,
        frm: ttk.Frame,
        row: int,
        column: int,
        columnspan: int,
        proj_path: str,
        refresh: callable,
    ):
        super().__init__(frm, values=["Refresh"], state="readonly")
        self.set(proj_path)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="ew")

        def _refresh(event):
            self.set(proj_path)
            refresh()

        self.bind("<<ComboboxSelected>>", _refresh)
