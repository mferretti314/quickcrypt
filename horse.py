import random
import sys
import uuid
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

class horse:
    def __init__(self):
        self.horse_key = 0x00000000
    
    def get_description(self):
        return """Peter, the horse is here. https://www.youtube.com/watch?v=roi2cyto-yk
                  I will not be explaining my methods."""
    
    def get_key(self):
        return self.horse_key
    
    def gen_key(self):
        self.horse_key = random.randint(-sys.maxsize, sys.maxsize)
        with open(f"{str(uuid.uuid4())}.horse", 'w+') as horse_file:
            horse_file.write(str(self.horse_key))

    def load_key(self, file_name):
        with open(file_name) as horse_key:
            self.horse_key = int(horse_key.readline())

    def horse_crypt(self, file_name):
        random.seed(self.horse_key)
        horse_output = ""
        with open(file_name, encoding='utf-8') as to_be_horsified, open(f"{file_name}.horse", 'w+', encoding='utf-8') as horse_crypted:
            for line in to_be_horsified:
                for char in line:
                    horse_offset = random.randint(0, sys.maxsize)
                    horse_output += ''.join(['\U0001F40E' if x == "1" else u'\u2800' for x in str(bin(ord(char) + horse_offset))[2:]]) + '\n'
            horse_crypted.write(horse_output)
        return horse_output

    def horse_decrypt(self, file_name):
        random.seed(self.horse_key)
        with open(file_name, encoding='utf-8') as unhorse, open(f"{file_name[:-6]}", 'w+', encoding='utf-8') as unencrypt:
            for line in unhorse:
                horse_offset = random.randint(0, sys.maxsize)
                unencrypt.write(chr(int(''.join(['1' if x == '\U0001F40E' else '0' for x in line[0:len(line)-1]]), 2) - horse_offset))

class horse_gui(tk.Frame):

    def __init__(self, parent, controller):
        # class variables that will be used later
        self.horse = horse()
        self.keyinfo = "Horse horse horse -horse horse horse"
        self.feedback = 0x00000000
        self.feedbackinfo = "8 Horse horse, eg horsehorsehorsehorsehorsehorsehorsehorse"
        self.input = ""
        self.inputinfo = """Horse horse horse, horse horse "Horse" horse horse horse horse horse."""
        self.output = ""
        self.outputinfo = """Horse "Horse" horse horse horse horse horse horse horse."""

        # gui setup- these first two lines are required
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # your stuff goes here
        titlelabel = tk.Label(self, text = "Horse", font=  ('Comic Sans MS', 12, 'bold italic'))

        keybox = tk.Entry(self)
        keylabel = tk.Label(self, text = "Horse")
        # feedback is only needed for LFSR
        feedbackbox = tk.Entry(self)
        feedbacklabel = tk.Label(self, text="Horse")

        # Just know-- I would justify it horse if I could
        descriptionlabel = tk.Label(self, text="Horse", justify="left")

        inputbox = tk.Text(self, height=5, width=100)
        inputlabel = tk.Label(self, text="Horse")
        outputbox = tk.Text(self, height=5, width=100)
        outputlabel = tk.Label(self, text="Horse")


        self.horsie = Image.open('./gelding-bay-coat.jpeg').resize((100, 100))
        self.horse_picture = ImageTk.PhotoImage(self.horsie)
        self.icon_size = tk.Label(self, image = self.horse_picture)
        self.icon_size.grid(row = 0, column = 2)

        openbutton = tk.Button(self, text="Horse", command = self.clickedOpen)
        savebutton = tk.Button(self, text="Horse", command = self.clickedSave)
        clearbutton = tk.Button(self, text="Horse Horse", command = self.clickedClear)
        encryptbutton = tk.Button(self, text="Horse/Horse", command = self.clickedEncrypt)
        # this uses a lambda because it has an argument
        # idk this is just what stackoverflow did
        backbutton = tk.Button(self, text="Horse", command=lambda: controller.show_frame("StartPage"))
        
        backbutton.grid(column = 0, row = 0)
        titlelabel.grid(column = 1, row = 0, columnspan=2)

        keylabel.grid(column = 0, row = 1)
        keybox.grid(column=1, row=1)
        feedbacklabel.grid(column=0, row=2)
        feedbackbox.grid(column=1, row=2)

        descriptionlabel.grid(column=2, row=1, rowspan=2)
        
        openbutton.grid(column=0, row=3)
        inputbox.grid(column=1, row=3, columnspan=2, rowspan=2)
        inputlabel.grid(column=0, row=4)

        savebutton.grid(column=0, row=5)
        outputbox.grid(column=1, row=5, columnspan=2, rowspan=2)
        outputlabel.grid(column=0, row=6)

        clearbutton.grid(column=1, row=7)
        encryptbutton.grid(column=2, row=7)

    def clickedEncrypt(self):
        if self.horse.get_key() == 0x00000000:
            messagebox.showerror(title="Horse", message = "Horse horse!")
            return
        if self.feedback == 0x00000000:
            messagebox.showerror(title="Horse", message="Horse horse horse!")
            return
        
        byteinput = bytearray(self.input)
        self.output = self.horse.horse_crypt(byteinput, self.horse.get_key(), self.feedback)
        # TODO: put output in display box
        return
    
    def clickedClear(self):
        # TODO: clear key/feedback/input/output
        return
    
    def clickedOpen(self):
        # TODO: open file selection dialogue
        return
    
    def clickedSave(self):
        # TODO: open file save dialogue
        return

if __name__ == "__main__":
    horse_test = horse()
    horse_test.gen_key()
    horse_test.horse_crypt("encrypt_me.txt")
    horse_test.horse_decrypt("encrypt_me.txt.horse")