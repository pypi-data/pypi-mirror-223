# http://tkdocs.com/tutorial/morewidgets.html#text
# https://docs.python.org/3/library/tkinter.html

import os
import sys

from tkinter import (
    Tk,
    ttk,
)

from . import widgets


class Grid(list):
    def __init__(self, frm):
        super().__init__()
        self.padding = 10
        self.column_span = 2
        self.frm: ttk.Frame = frm

    def add_partial_widget(self, widget: callable, kwargs: dict, label: str = ""):
        row = len(self)
        if label:
            instance = [
                widgets.Label(
                    frm=self.frm,
                    text=label,
                    row=row,
                    column=0,
                    columnspan=1,
                    pady=self.padding,
                ),
                widget(
                    frm=self.frm,
                    row=row,
                    column=1,
                    columnspan=self.column_span - 1,
                    **kwargs
                ),
            ]
            self.append(instance)
            return instance[1]
        else:
            instance = [
                widget(
                    frm=self.frm,
                    row=row,
                    column=0,
                    columnspan=self.column_span,
                    **kwargs
                )
            ]
            self.append(instance)
            return instance[0]


class App:
    def __init__(self, root: Tk, proj_path: str) -> None:
        self.root: Tk = root
        self.root.title("Setup project")
        self.proj_path: str = os.path.abspath(proj_path) if proj_path else os.getcwd()

        self.actions: dict[str, list] = {"startup": [], "refresh": []}
        self.grid: Grid = None

        self.setup_frame()
        self.setup_grid()
        self.do_startup()

    def setup_frame(self):
        padding = 10
        frm = ttk.Frame(self.root, padding=padding)
        frm.grid(sticky="news")
        self.grid = Grid(frm)

        self.root.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

    def setup_grid(self):
        self.progress: widgets.WorkerProgress = self.grid.add_partial_widget(
            label="Log:", widget=widgets.WorkerProgress, kwargs={}
        )
        self.log: widgets.Log = self.grid.add_partial_widget(
            widget=widgets.Log, kwargs={}
        )
        self.quit: widgets.ButtonQuit = self.grid.add_partial_widget(
            widget=widgets.ButtonQuit,
            kwargs={"pady": self.grid.padding, "quit": self.destroy},
        )

    def iterate_generator(self, iterable=None, progress_steps=0) -> None:
        if progress_steps:
            self.progress.progress_steps = progress_steps
            self.progress.set(0)
        try:
            self.progress.step(self.progress.progress_steps)
            next(iterable)
            self.root.after(10, self.iterate_generator, iterable)
        except StopIteration:
            self.progress.set(100)

    def run_generator(
        self, iterable: callable, wait: int = 10, progress_steps: int = 10
    ):
        self.root.after(wait, self.iterate_generator, iterable, progress_steps)

    def do_startup(self):
        def gen():
            result = []
            yield
            if sys.version_info < (3, 10, 0):
                result.append(
                    "ERROR: Python3 is outdated. "
                    "Please download and install Python 3.10 or newer from python.org"
                )
                # self.startup_state.set(result[-1])
                self.log.append(result[-1])
            yield
            for action in self.actions["startup"]:
                action(result)
                yield
            if result:
                self.startup_state.set("\n".join(result))
            else:
                self.startup_state.set("OK")
            self.do_refresh()

        self.run_generator(gen(), wait=500)

    def do_refresh(self):
        os.chdir(self.proj_path)

        def gen():
            yield
            for action in self.actions["refresh"]:
                action()
            yield

        self.run_generator(gen())

    # def generator_install(self):
    #     pass

    def generator_cancel(self):
        pass

    def destroy(self):
        self.generator_cancel()
        self.root.destroy()

    def log_append(self, text: str, end: str = "\n"):
        self.log.append(text, end)


def main(proj_path: str):
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", App(root, proj_path).destroy)
    root.mainloop()
