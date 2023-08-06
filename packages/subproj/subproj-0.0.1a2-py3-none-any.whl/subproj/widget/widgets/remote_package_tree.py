from tkinter import ttk, Menu, Event


class RemotePackageTree(ttk.Treeview):
    def __init__(
        self,
        frm: ttk.Frame,
        row: int,
        column: int,
        columnspan: int,
        install: callable,
    ):
        super().__init__(frm, columns=["serial"], displaycolumns="#all")
        self.heading("#0", text="Package / Version")
        self.heading("serial", text="Date / Serial")
        frm.rowconfigure(row, weight=1)
        self.grid(row=row, column=column, columnspan=columnspan, sticky="news")

        self.menu_remote = Menu(frm, tearoff=0)
        self.menu_remote.add_command(label="Install package", command=install)

        def _menu(event: Event):
            iid = self.identify_row(event.y)
            if iid:
                self.selection_set(iid)
                if self.item(iid)["values"]:
                    self.menu_remote.post(event.x_root, event.y_root)
                else:
                    self.item(iid, open=True)

        self.bind("<Button-3>", _menu)
