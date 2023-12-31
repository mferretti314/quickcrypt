import random
import sys
import uuid
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import filedialog

name = "horse"
description = """horse"""

class horse:
    def __init__(self):
        self.horse_key = random.randint(0, 50000)

    def get_description(self):
        return """Peter, the horse is here. https://www.youtube.com/watch?v=roi2cyto-yk
                  I will not be explaining my methods."""
    
    def set_key(self, key):
        self.horse_key = key

    def get_key(self):
        return self.horse_key

    def horse_crypt(self, data):
        horse_output = ""
        data = list(data)
        for char in data:
            horse_output += ''.join(['\U0001F40E' if x == "1" else u'\u2800' for x in str(bin(char + self.horse_key))[2:]]) + '\n'
        return horse_output

    def horse_decrypt(self, data):
        horse_output = ""
        data = data.decode().split('\n')
        loc_key = int(self.horse_key)
        while ('' in data):
            data.remove('')
        for line in data:
            horse_output += chr(int(''.join(['1' if x == '\U0001F40E' else '0' for x in line]),2) - loc_key)
        return horse_output

class horse_gui(tk.Frame):

    def __init__(self, parent, controller):
        # class variables that will be used later
        self.data = bytearray()
        self.key = ""
        self.usefileinput = False

        self.input = ""
        self.output = ""

        # gui setup- these first two lines are required
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # your stuff goes here
        self.titlelabel = tk.Label(self, text=name, font=controller.title_font)

        self.entry_text = tk.StringVar()
        self.keybox = tk.Entry(self, textvariable = self.entry_text)
        self.entry_text.set("")
        self.keylabel = tk.Label(self, text="Key")

        self.descriptionlabel = tk.Label(self, text=description, justify="left", borderwidth=3, relief="sunken", pady=3)

        self.inputbox = tk.Text(self, height=5, width=100)
        self.inputlabel = tk.Label(self, text="Input")
        self.outputbox = tk.Text(self, height=5, width=100)
        self.outputlabel = tk.Label(self, text="Output")

        self.horsie = Image.open('./gelding-bay-coat.jpeg').resize((100, 100))
        self.horse_picture = ImageTk.PhotoImage(self.horsie)
        self.icon_size = tk.Label(self, image = self.horse_picture)
        self.icon_size.grid(row = 0, column = 2)

        self.openbutton = tk.Button(self, text="Open", command=self.clickedOpen)
        self.savebutton = tk.Button(self, text="Save", command=self.clickedSave)
        self.clearbutton = tk.Button(self, text="Clear Fields", command=self.clickedClear)
        self.encryptbutton = tk.Button(self, text="Encrypt", command=self.clickedEncrypt)
        self.decryptbutton = tk.Button(self, text="Decrypt", command=self.clickedDecrypt)
        # this uses a lambda because it has an argument
        # idk this is just what stackoverflow did
        self.backbutton = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))

        self.backbutton.grid(column=0, row=0)
        self.titlelabel.grid(column=1, row=0, columnspan=2)

        self.keylabel.grid(column=0, row=1)
        self.keybox.grid(column=1, row=1)

        self.descriptionlabel.grid(column=2, row=1, rowspan=2, pady=3, sticky='nsew')

        self.openbutton.grid(column=0, row=4)
        self.inputbox.grid(column=1, row=3, columnspan=2, rowspan=2, sticky='nsew', padx=3, pady=3)
        self.inputlabel.grid(column=0, row=3)

        self.savebutton.grid(column=0, row=6)
        self.outputbox.grid(column=1, row=5, columnspan=2, rowspan=2, sticky='nsew', padx=3, pady=3)
        self.outputlabel.grid(column=0, row=5)

        self.clearbutton.grid(column=1, row=7, pady=5)
        self.encryptbutton.grid(column=2, row=7, pady=5)
        self.decryptbutton.grid(column=2, row=8, pady=5)

    def clickedEncrypt(self):
        # converts an escape sequence entry (like "\x01\x02text\xff") to an array of bytes
        # we only need to update the input bytes if we're not using a file
        # since the file input code already updates it
        data = ''
        if not self.usefileinput:
            self.input = self.inputbox.get(1.0, tk.END)

            data = self.input
            data = data[:-1]
            data = data.encode()
            data = data.decode('unicode_escape').encode("raw_unicode_escape")
        else:
            data = self.input

        
        horser = horse()
        horsetext = horser.horse_crypt(data)
        self.entry_text.set(horser.get_key())
        # ciphertext

        self.output = horsetext
        # clear and write output to the display box
        # would normally display as "bytearray(stuff)" so the [12:-2] chops the extra stuff off
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output))
        return

    def clickedDecrypt(self):
        if len(self.keybox.get()) <= 0:
            messagebox.showerror(title="Key Error",
                                 message="Key needs to be atleast 1 character long.")
            return

        # converts an escape sequence entry (like "\x01\x02text\xff") to an array of bytes
        # we only need to update the input bytes if we're not using a file
        # since the file input code already updates it
        data = ''
        if not self.usefileinput:
            self.input = self.inputbox.get(1.0, tk.END)
            data = self.input
            data = data[:-1]
            data = data.encode()
            data = data.decode('unicode_escape').encode("raw_unicode_escape")
        else:
            data = self.input

        key = self.keybox.get()
        key = bytes(str(key), 'utf-8')
        horser = horse()
        horser.set_key(key.decode())
        self.output = horser.horse_decrypt(data)

        # clear and write output to the display box
        # would normally display as "bytearray(stuff)" so the [12:-2] chops the extra stuff off
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output))
        return

    def clickedClear(self):
        # TODO: clear key/input/output
        self.keybox.delete(0, tk.END)
        # the text box widgets have a slightly different clearing method than the one-line entry widgets
        # gotta re-enable it first because disabled state applies to everything, not just user typing
        self.inputbox.config(state="normal")
        self.inputbox.delete(1.0, tk.END)
        self.outputbox.delete(1.0, tk.END)
        self.usefileinput = False

        return

    def clickedOpen(self):
        filename = filedialog.askopenfilename(
            filetypes=(("Text files", "*.txt*"), ("all files", "*.*"))
        )
        if filename == None:
            return
        self.inputbox.delete('1.0', tk.END)
        self.inputbox.insert('1.0',
                             filename + "\n\nIn file mode. Press \"Clear Fields\" to return to normal text entry mode.")
        file = open(filename, 'rb')
        self.input = file.read()
        file.close()
        self.usefileinput = True
        return

    def clickedSave(self):
        # TODO: open file save dialogue
        file = filedialog.asksaveasfile(mode='wb')
        file.write(self.output)
        file.close()
        return