from tkinter import ttk, Menu, Event


class LocalSubprojTree(ttk.Treeview):
    def __init__(
        self,
        frm: ttk.Frame,
        row: int,
        column: int,
        columnspan: int,
        install: callable,
        remove: callable,
    ):
        super().__init__(
            frm,
            height=6,
            columns=["package", "version", "state"],
            displaycolumns="#all",
        )
        self.heading("#0", text="Path")
        self.heading("package", text="Package")
        self.heading("version", text="Version")
        self.heading("state", text="State")
        frm.rowconfigure(row, weight=1)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="news")
        self.menu = Menu(frm, tearoff=0)
        self.menu.add_command(label="Install package", command=install)
        self.menu.add_command(label="Remove package", command=remove)

        def _menu(event: Event):
            iid = self.identify_row(event.y)
            if iid:
                self.selection_set(iid)
                self.menu.post(event.x_root, event.y_root)

        self.bind("<Button-3>", _menu)
