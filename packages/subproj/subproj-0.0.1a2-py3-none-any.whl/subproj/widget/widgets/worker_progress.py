from tkinter import ttk, HORIZONTAL, DoubleVar


class WorkerProgress(ttk.Progressbar):
    def __init__(self, frm: ttk.Frame, row: int, column: int, columnspan: int):
        self.progress_value = DoubleVar(frm, 0.0)
        self.progress_steps = 1

        super().__init__(
            frm,
            orient=HORIZONTAL,
            mode="determinate",
            variable=self.progress_value,
        )

        self.grid(row=row, column=column, columnspan=columnspan, sticky="ew")

    def set(self, value: float):
        self.progress_value.set(value)
