import tkinter as tk
from tkinter import *
from tkinter import font as tkfont

import sym_LFSR, asym_RSA
import horse

# this is the main driver for the window. don't touch this!
# this is how you swap UI layouts without opening a new window
class QuickCrypt(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family="Calibri", size=18, weight="bold", slant="roman")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, sym_LFSR.LFSR_gui, horse.horse_gui, asym_RSA.RSA_gui):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        self.geometry("")
        frame = self.frames[page_name]
        frame.tkraise()
        
# this is basically a template class for a window setup, or "frame" as they're called in tk
# shove your selector UI code in here
class StartPage(tk.Frame):
    # python constructor, executed on creation
    def __init__(self, parent, controller):
        # initialize the tk frame stuff
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Title prompt
        label = tk.Label(self, text="Select your cipher below:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        #Spacing
        spacer = tk.Label(self, text="")
        spacer.pack()

        #List of options to encrypt/decrypt
        OPTIONS_DICT = {
            "AES (Symmetric)":"AES_gui",
            "DES (Symmetric)":"DES_gui",
            "LFSR (Symmetric)":"LFSR_gui",
            "Rotational (Symmetric)":"ROT_gui",
            "RSA (Asymmetric)":"RSA_gui",
            "SHA-1 (Hash)":"SHA1_gui",
            "SHA-2 (Hash)":"SHA2_gui",
            "SHA-3 (Hash)":"SHA3_gui",
            "BLAKE2 (Hash)":"BLAKE2_gui",
            "MD5 (Hash)":"MD5_gui",
            "horse (horse)":"horse_gui"
        }
        opts = list(OPTIONS_DICT.keys())
        #Setup drop down menu
        variable = StringVar(self)
        variable.set(opts[0])
        self.w = OptionMenu(self, variable, *opts)
        self.w.pack()

        #Spacing
        spacer2 = tk.Label(self, text="")
        spacer2.pack()

        #Compares what has been selected to whats in the list to take users to there page they selected
        def page_select():
            controller.show_frame(OPTIONS_DICT[variable.get()])

        #Jumps to whatever page was selected
        button_select = tk.Button(self, text="Select", command=page_select)
        button_select.pack()

        #the "command=" bit will open the frame from the class that matches the text in the string- see sym_LFSR.py

# main function. you shouldn't need to touch this.
if __name__ == "__main__":
    app = QuickCrypt()
    app.mainloop()
