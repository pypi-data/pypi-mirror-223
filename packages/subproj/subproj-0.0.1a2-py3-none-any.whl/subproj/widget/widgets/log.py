from tkinter import scrolledtext, ttk, END


class Log(scrolledtext.ScrolledText):
    def __init__(self, frm: ttk.Frame, row: int, column: int, columnspan: int):
        super().__init__(frm, height=6)
        frm.rowconfigure(row, weight=1)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="news")

    def append(self, text: str, end: str = "\n"):
        self.insert(END, f"{text}{end}")
        self.see(END)
