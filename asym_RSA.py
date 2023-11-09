import tkinter as tk
import codecs
from tkinter import messagebox
from tkinter import filedialog
from Crypto.PublicKey import RSA


name = "RSA"

description = """A high-security asymmetric cipher. Uses different keys to encrypt and decrypt.
Uses a public key based on the product of two secret prime numbers to encode data.
Public keys can be sent over unsecured lines of communication.
Messages can be encrypted by anyone who knows the recipient's public key. 
Messages can only be decrypted with the private key- the secret prime numbers.
Fairly slow; usually used to send a key for a faster symmetric cipher like AES."""


# this defines the UI for the cipher
# when I'm done with it you should be able to copy and paste it without a ton of reconfiguring
class RSA_gui(tk.Frame):

    def __init__(self, parent, controller):
        # class variables that will be used later
        self.data = bytearray()
        self.key = None
        self.publickey = None
        self.privatekey = None
        self.usefileinput = False

        self.input = ""
        self.output = ""

        # gui setup- these first two lines are required
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # your stuff goes here
        self.titlelabel = tk.Label(self, text=name, font=controller.title_font)

        self.openpubbutton = tk.Button(self, text="Open Public Key\n(public.pem)", height=2, width=13, command=self.clickedLoadPub)
        self.openprivbutton = tk.Button(self, text="Open Private Key\n(private.pem)", height=2, width=13, command=self.clickedLoadPriv)
        self.genkeysbutton = tk.Button(self, text="Generate Keys", command = self.clickedGenerate, height=2, width=13)

        self.keyinfobox = tk.Label(self, text="No keys loaded. Cannot encrypt or decrypt.", justify="left", borderwidth=3, relief="sunken", pady=3)

        self.descriptionbox = tk.Label(self, text=description, justify="left", borderwidth=3, relief="sunken", pady=3, height=7)

        self.inputbox = tk.Text(self, height=5, width=100)
        self.inputlabel = tk.Label(self, text="Input")
        self.outputbox = tk.Text(self, height=5, width=100)
        self.outputlabel = tk.Label(self, text="Output")

        self.openbutton = tk.Button(self, text="Open", command = self.clickedOpen)
        self.savebutton = tk.Button(self, text="Save", command = self.clickedSave)
        self.clearbutton = tk.Button(self, text="Clear Fields", command = self.clickedClear)
        self.encryptbutton = tk.Button(self, text="Encrypt", command = self.clickedEncrypt)
        self.decryptbutton = tk.Button(self, text="Decrypt", command= self.clickedDecrypt)
        # this uses a lambda because it has an argument
        # idk this is just what stackoverflow did
        self.backbutton = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        
        self.backbutton.grid(column = 0, row = 0)
        self.titlelabel.grid(column = 1, row = 0, columnspan=3)

        self.openpubbutton.grid(row=1, column=1, pady=3)
        self.openprivbutton.grid(row=1, column=2, pady=3)
        self.genkeysbutton.grid(row=1, column=0, pady=3, padx=3)

        self.descriptionbox.grid(row=1, column=3, rowspan=2, columnspan=2, pady=5, padx=3)
        self.keyinfobox.grid(row=2, column=0, columnspan=3, pady=5, sticky="nsew", padx=3)
        
        
        self.inputbox.grid(row=3, column=1, columnspan=3, rowspan=2, pady=3)
        self.inputlabel.grid(row=3, column=0)
        self.openbutton.grid(row=4, column=0)

        self.outputbox.grid(column=1, row=5, columnspan=3, rowspan=2,pady=3)
        self.outputlabel.grid(column=0, row=5)
        self.savebutton.grid(column=0, row=6)

        self.clearbutton.grid(column=1, row=7, pady=3)
        self.decryptbutton.grid(column=2, row=7, pady=3)
        self.encryptbutton.grid(column=3, row=7, pady=3)
    
    def clickedLoadPub(self):
        return
    
    def clickedLoadPriv(self):
        return

    def clickedGenerate(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        # get file write location
        file = filedialog.asksaveasfile(mode='wb', initialfile="private.pem", title="Save private key", filetypes=(("Key file","*.pem*")))
        file.write(private_key)
        file.close()

        public_key = key.public_key().export_key()
        file = filedialog.asksaveasfile(mode='wb', initialfile="public.pem", title="Save public key", filetypes=(("Key file","*.pem*")))
        file.write(public_key)
        file.close()

        self.privatekey = private_key
        self.publickey = public_key

        return
    
    def clickedEncrypt(self):
        # checking the text -> int conversion for key/feedback
        #messagebox.showerror(title="Key Error", message="Could not convert " + self.keybox.get() + " to hexadecimal. Please use a format like 0x1234ABCD.")
        #messagebox.showerror(title="Feedback Error", message="Could not convert " + self.feedbackbox.get() + " to hexadecimal. Please use a format like 0x1234ABCD.")
        
        # converts an escape sequence entry (like "\x01\x02text\xff") to an array of bytes
        # we only need to update the input bytes if we're not using a file
        # since the file input code already updates it
        if not self.usefileinput:
            self.input = self.inputbox.get(1.0, tk.END)
            self.input = bytearray(codecs.escape_decode(self.input)[0])

        #self.output = encrypt(self.input, self.key, self.feedback)
        # clear and write output to the display box
        # would normally display as "bytearray(stuff)" so the [12:-2] chops the extra stuff off
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output)[12:-2])
        return
    
    def clickedDecrypt(self):
        return
    
    def clickedClear(self):
        # TODO: clear key/feedback/input/output
        #self.keybox.delete(0, tk.END)
        #self.feedbackbox.delete(0, tk.END)
        # the text box widgets have a slightly different clearing method than the one-line entry widgets
        # gotta re-enable it first because disabled state applies to everything, not just user typing
        self.inputbox.config(state="normal")
        self.inputbox.delete(1.0, tk.END)
        self.outputbox.delete(1.0, tk.END)
        self.usefileinput = False
        
        return
    
    def clickedOpen(self):
        filename = filedialog.askopenfilename(
            filetypes = (("Text files","*.txt*"),("all files", "*.*"))
        )
        if filename == None:
            return
        self.inputbox.delete('1.0', tk.END)
        self.inputbox.insert('1.0', filename + "\n\nIn file mode. Press \"Clear Fields\" to return to normal text entry mode.")
        file = open(filename, 'rb')
        self.input = file.read()
        file.close()
        self.usefileinput = True
        # prevents typing in the box
        self.inputbox.config(state="disabled")
        return
    
    def clickedSave(self):
        # TODO: open file save dialogue
        file = filedialog.asksaveasfile(mode='wb')
        file.write(self.output)
        file.close()
        return