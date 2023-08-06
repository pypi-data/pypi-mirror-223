from tkinter import (
    Tk,
    ttk,
    messagebox,
    Text,
    LEFT,
    W,
    TOP,
    BOTH,
    INSERT,
    END,
    FLAT,
    DISABLED,
)


class Application(ttk.Frame):
    def save(self):
        msg = self.commit.get("0.0", END).encode("utf8")
        if msg.strip() == "":
            messagebox.showwarning("Advarsel", "Melding kan ikke være tom")
        else:
            open(self.filename, "w").writelines((msg, self.file_content))
            self.quit()

    def createWidgets(self):
        # self.filename = '''$(FILENAME)'''
        self.filename = """commit_message_example.txt"""
        self.file_content = open(self.filename, "r").read()

        self.headline = ttk.Label(
            self,
            height=1,
            text="Kort beskrivelse av endringene:",
            anchor=W,
            justify=LEFT,
        )
        self.headline.pack(side=TOP, fill=BOTH)

        self.commit = Text(self, height=6, width=100, background="white", fg="black")
        self.commit.pack(side=TOP, fill=BOTH)
        self.commit.focus()
        self.commit.bind("<Return>", (lambda event: self.save()))
        self.commit.bind("<Escape>", (lambda event: self.quit()))

        self.info = Text(self, height=20, relief=FLAT)

        try:
            self.info.insert(
                INSERT, self.file_content[self.file_content.index("HG: --") + 7 :]
            )
        except ValueError:
            self.info.insert(INSERT, self.file_content)
        finally:
            self.info.config(state=DISABLED)

        self.info.pack(side=TOP, fill=BOTH)

        self.save_button = ttk.Button(self, text="Lagre", command=self.save)
        self.save_button.pack(side=LEFT)

        self.cancel_button = ttk.Button(self, text="Avbryt", command=self.quit)
        self.cancel_button.pack(side=LEFT)

    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=BOTH)
        self.createWidgets()


root = Tk()
root.title("Sjekk inn")
app = Application(master=root)
app.mainloop()
root.destroy()
