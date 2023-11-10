import tkinter as tk
import codecs, binascii
from tkinter import messagebox
from tkinter import filedialog
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


name = "RSA"

description = """A high-security asymmetric cipher. Uses different keys to encrypt and decrypt messages.
Relies on a linked pair of keys- public and private. A message is encrypted using the 
recipient's public key, and decrypted using their private key. Public keys can be sent 
over unsecure channels, but private keys should never be shared. The algorithm is slow
and limited to 190 characters. It's usually used to exchange a key for another cipher."""


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
        filename = filedialog.askopenfilename(
            filetypes = (("Public key","*.pem*"),("all files", "*.*"))
        )
        if filename == None:
            return
        file = open(filename, 'rb')
        self.publickey = RSA.import_key(file.read())
        file.close()

        if self.privatekey is not None:
            self.keyinfobox.config(text="Public and private keys loaded. Ready to encrypt or decrypt.")
        elif self.publickey is not None:
            self.keyinfobox.config(text="Public key loaded. Ready to encrypt.")
        else:
            self.keyinfobox.config(text="Error loading public key.")
        return
    
    def clickedLoadPriv(self):
        filename = filedialog.askopenfilename(
            filetypes = (("Private key","*.pem*"),("all files", "*.*"))
        )
        if filename == None:
            return
        file = open(filename, 'rb')
        self.privatekey = RSA.import_key(file.read())
        file.close()

        if self.publickey is not None:
            self.keyinfobox.config(text="Public and private keys loaded. Ready to encrypt or decrypt.")
        else:
            self.keyinfobox.config(text="Private key loaded. Ready to decrypt.")
        return

    def clickedGenerate(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        # get file write location
        file = filedialog.asksaveasfile(mode='wb', initialfile="private.pem", title="Save private key", filetypes=(("Key files","*.pem*"),("all files", "*.*")))
        file.write(private_key)
        file.close()

        public_key = key.public_key().export_key()
        file = filedialog.asksaveasfile(mode='wb', initialfile="public.pem", title="Save public key", filetypes=(("Key files","*.pem*"),("all files", "*.*")))
        file.write(public_key)
        file.close()

        self.privatekey = private_key
        self.publickey = public_key
        self.keyinfobox.config(text="Public and private keys loaded. Ready to encrypt or decrypt.")

        return
    
    def clickedEncrypt(self):
        if self.publickey is None:
            messagebox.showerror(title="Key Error", message="No public key loaded.")

        if not self.usefileinput:
            self.input = self.inputbox.get(1.0, tk.END)
            self.input = bytearray(codecs.escape_decode(self.input)[0])

        
        cipher_rsa = PKCS1_OAEP.new(self.publickey)
        
        self.output = cipher_rsa.encrypt(self.input)
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output)[2:-1])

        return
    
    def clickedDecrypt(self):
        if self.privatekey is None:
            messagebox.showerror(title="Key Error", message="No private key loaded.")

        if not self.usefileinput:
            self.input = self.inputbox.get(1.0, tk.END)
            # try decoding hex to bytes first
            #try:
                #print(self.input)
                #s = binascii.unhexlify(self.input.strip())
                #self.input = s
            #except:
                # otherwise just do the normal conversion
                #print("couldn't convert input from hex to bytes")
            self.input = bytearray(codecs.escape_decode(self.input.strip())[0])


        print(len(self.input))
        cipher_rsa = PKCS1_OAEP.new(self.privatekey)
        self.output = cipher_rsa.decrypt(self.input)
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output)[2:-1])
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
        self.publickey = None
        self.privatekey = None
        self.keyinfobox.config(text="No keys loaded. Cannot encrypt or decrypt.")
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