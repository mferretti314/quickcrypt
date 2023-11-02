import tkinter as tk
import codecs
from tkinter import messagebox
from tkinter import filedialog
from Crypto.Cipher import AES

name = "AES"

description = """The Advanced Encryption Standard (AES) is a symmetric block cipher chosen by the U.S. 
government to protect classified information. AES is implemented in software and hardware 
throughout the world to encrypt sensitive data. AES is a variant of Rijndael, with a fixed 
block size of 128 bits, and a key size of 128, 192, or 256 bits."""

# this defines the UI for the cipher
# when I'm done with it you should be able to copy and paste it without a ton of reconfiguring
class AES_gui(tk.Frame):

    def __init__(self, parent, controller):
        # class variables that will be used later
        self.data = bytearray()
        self.key = ""
        self.nonce = ""
        self.usefileinput = False

        self.input = ""
        self.output = ""

        # gui setup- these first two lines are required
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # your stuff goes here
        self.titlelabel = tk.Label(self, text=name, font=controller.title_font)

        self.keybox = tk.Entry(self)
        self.keylabel = tk.Label(self, text="Key")

        #Nonce neeeded for AES Decryption
        self.noncebox = tk.Entry(self)
        self.noncelabel = tk.Label(self, text="Nonce")

        self.descriptionlabel = tk.Label(self, text=description, justify="left", borderwidth=3, relief="sunken", pady=3)

        self.inputbox = tk.Text(self, height=5, width=100)
        self.inputlabel = tk.Label(self, text="Input")
        self.outputbox = tk.Text(self, height=5, width=100)
        self.outputlabel = tk.Label(self, text="Output")

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
        self.noncelabel.grid(column=0, row=2)
        self.noncebox.grid(column=1, row=2)

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
        if len(self.keybox.get()) != 16 and len(self.keybox.get()) != 24 and len(self.keybox.get()) != 32:
            messagebox.showerror(title="Key Error",
                                 message="Key needs to be either 16, 24, or 32 characters long.")
            return

        # converts an escape sequence entry (like "\x01\x02text\xff") to an array of bytes
        # we only need to update the input bytes if we're not using a file
        # since the file input code already updates it
        self.input = self.inputbox.get(1.0, tk.END)

        data = self.input
        data = data[:-1]
        data = data.encode()
        data = data.decode('unicode_escape').encode("raw_unicode_escape")

        key = self.keybox.get()
        key = bytes(str(key), 'utf-8')

        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        self.nonce = nonce
        self.output = ciphertext
        # clear and write output to the display box
        # would normally display as "bytearray(stuff)" so the [12:-2] chops the extra stuff off
        self.noncebox.delete(0, tk.END)
        self.noncebox.insert(0, str(self.nonce)[2:-1])
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output)[2:-1])
        return

    def clickedDecrypt(self):
        if len(self.keybox.get()) != 16 and len(self.keybox.get()) != 24 and len(self.keybox.get()) != 32:
            messagebox.showerror(title="Key Error",
                                 message="Key needs to be either 16, 24, or 32 characters long.")
            return

        # converts an escape sequence entry (like "\x01\x02text\xff") to an array of bytes
        # we only need to update the input bytes if we're not using a file
        # since the file input code already updates it
        self.input = self.inputbox.get(1.0, tk.END)

        data = self.input
        data = data[:-1]
        data = data.encode()
        data = data.decode('unicode_escape').encode("raw_unicode_escape")

        key = self.keybox.get()
        key = bytes(str(key), 'utf-8')

        nonce = self.noncebox.get()
        nonce = nonce.encode()
        nonce = nonce.decode('unicode_escape').encode("raw_unicode_escape")


        cipher = AES.new(key, AES.MODE_EAX, nonce)
        self.output = cipher.decrypt(data)

        # clear and write output to the display box
        # would normally display as "bytearray(stuff)" so the [12:-2] chops the extra stuff off
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output)[2:-1])
        return

    def clickedClear(self):
        # TODO: clear key/input/output
        self.keybox.delete(0, tk.END)
        self.noncebox.delete(0, tk.END)
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