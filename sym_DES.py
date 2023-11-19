
import tkinter as tk
from tkinter import messagebox, filedialog
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

name = "DES"

description = """TThe Data Encryption Standard (DES) is a symmetric-key cipher that encrypts digital data 
in 64-bit blocks using a 56-bit key. It executes complex transformations over 16 rounds, making it initially 
secure but later vulnerable to brute-force attacks due to its short key length. Although now superseded by more
advanced algorithms, DES was crucial in the development of cryptographic methods."""

class DES_Encryption:
    def __init__(self):
        self.key = None

    def generate_key(self):
        self.key = get_random_bytes(8)  # DES uses an 8-byte key
        return base64.b64encode(self.key).decode('utf-8')

    def encrypt(self, plaintext):
        cipher = DES.new(self.key, DES.MODE_ECB)
        padded_text = pad(plaintext.encode(), DES.block_size)
        encrypted = cipher.encrypt(padded_text)
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, ciphertext):
        cipher = DES.new(self.key, DES.MODE_ECB)
        decoded_text = base64.b64decode(ciphertext)
        decrypted = unpad(cipher.decrypt(decoded_text), DES.block_size)
        return decrypted.decode('utf-8')

    def set_key(self, key):
        self.key = base64.b64decode(key)

# GUI class for DES
class DES_gui(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.des = DES_Encryption()
        
        # GUI elements for DES encryption and decryption
        self.titlelabel = tk.Label(self, text=name, font=controller.title_font)
        self.keybox = tk.Entry(self)
        self.keylabel = tk.Label(self, text="Key")
        self.descriptionlabel = tk.Label(self, text=description, justify="left", borderwidth=3, relief="sunken", pady=3)
        self.inputbox = tk.Text(self, height=5, width=100)
        self.inputlabel = tk.Label(self, text="Input")
        self.encryptbutton = tk.Button(self, text="Encrypt", command=self.encrypt_message)
        self.decryptbutton = tk.Button(self, text="Decrypt", command=self.decrypt_message)
        self.outputbox = tk.Text(self, height=5, width=100)
        self.outputlabel = tk.Label(self, text="Output")
        self.openbutton = tk.Button(self, text="Open", command=self.clickedOpen)
        self.savebutton = tk.Button(self, text="Save", command=self.clickedSave)
        self.clearbutton = tk.Button(self, text="Clear Fields", command=self.clickedClear)

        self.backbutton = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))


        # Layout the widgets
        self.backbutton.grid(column=0, row=0)
        self.titlelabel.grid(column=1, row=0, columnspan=2)
        self.keylabel.grid(column=0, row=1)
        self.keybox.grid(column=1, row=1)
        self.descriptionlabel.grid(column=2, row=1, rowspan=2, pady=3, sticky='nsew')
        self.inputbox.grid(column=1, row=3, columnspan=2, rowspan=2, sticky='nsew', padx=3, pady=3)
        self.inputlabel.grid(column=0, row=3)
        self.outputbox.grid(column=1, row=5, columnspan=2, rowspan=2, sticky='nsew', padx=3, pady=3)
        self.outputlabel.grid(column=0, row=5)
        self.openbutton.grid(column=0, row=4)
        self.savebutton.grid(column=0, row=6)
        self.clearbutton.grid(column=1, row=7, pady=5)
        self.encryptbutton.grid(column=2, row=7, pady=5)
        self.decryptbutton.grid(column=2, row=8, pady=5)

    def encrypt_message(self):
        try:
            key = self.keybox.get()
            if len(key) != 12:
                raise ValueError("Key must be 8 bytes long (12 characters in Base64)")
            self.des.set_key(key)
            plaintext = self.inputbox.get("1.0", 'end-1c')
            encrypted_message = self.des.encrypt(plaintext)
            self.outputbox.delete("1.0", tk.END)
            self.outputbox.insert(tk.END, encrypted_message)
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def decrypt_message(self):
        try:
            key = self.keybox.get()
            if len(key) != 12:
                raise ValueError("Key must be 8 bytes long (12 characters in Base64)")
            self.des.set_key(key)
            ciphertext = self.inputbox.get("1.0", 'end-1c')
            decrypted_message = self.des.decrypt(ciphertext)
            self.outputbox.delete("1.0", tk.END)
            self.outputbox.insert(tk.END, decrypted_message)
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

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

