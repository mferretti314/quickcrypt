import tkinter as tk
from tkinter import font as tkfont

import sym_LFSR

class QuickCrypt(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family="Calibri", size=18, weight="bold", slant="roman")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, sym_LFSR.LFSR_gui):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text = "go to LFSR", command=lambda: controller.show_frame("LFSR_gui"))
        button.pack(side="bottom")

if __name__ == "__main__":
    app = QuickCrypt()
    app.mainloop()
