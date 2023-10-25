import tkinter as tk
import codecs
from tkinter import messagebox
from tkinter import filedialog

name = "LFSR"

description = """A Linear-Feedback Shift Register (LFSR) uses repeated bit shifts and XORs to encrypt data.
Medium security. Not incredibly cryptographically secure, but it's tricky to break in practice.
This is a symmetric cipher- both parties need the same key and feedback, and they must be shared securely.
Cannot be easily decrypted without either the key or the feedback value."""

def crypt(data, key, feedback):
    tempkey = key
    shift(tempkey, feedback)
    bytedata = bytearray()

    if type(data) is str:
        bytedata = bytearray(data, 'utf-8')
    else:
        bytedata = bytearray(data)

    for i in range(0, len(bytedata)):
        bytedata[i] = (bytedata[i] ^ tempkey) & 0xFF
        tempkey = shift(tempkey, feedback)
        
    return bytedata

def shift(tempkey, feedback):
    for x in range(0,8):
        tempkey = minishift(tempkey, feedback)
    return tempkey
    
def minishift(tempkey, feedback):
    if (tempkey & 1 == 1):
        return (tempkey >> 1)
    else:
        return (tempkey >> 1) ^ feedback
        
def test():
    output = crypt('encrypt me', 0x12345678, 0x87654321)
    print(output)
    reverse = crypt(output, 0x12345678, 0x87654321)
    print(reverse)
    print(" ")
    with open('encrypt_me.txt',mode='rb') as file:
        filedata = bytearray(file.read())
        output = crypt(filedata, 0x12345678, 0x87654321)
        print(output)
        print(crypt(output, 0x12345678, 0x87654321))

# this defines the UI for the cipher
# when I'm done with it you should be able to copy and paste it without a ton of reconfiguring
class LFSR_gui(tk.Frame):

    def __init__(self, parent, controller):
        # class variables that will be used later
        self.data = bytearray()
        self.key = 0x00000000
        self.keyinfo = "8 hexadecimal digits, eg 0x1234ABCD"
        self.feedback = 0x00000000
        self.feedbackinfo = "8 hexadecimal digits, eg 0xF1E2D3C4"
        self.usefileinput = False

        self.input = ""
        self.inputinfo = """Type text here, or select "Open" to choose an input file."""
        self.output = ""
        self.outputinfo = """Click "Save" to save this output to a file."""

        # gui setup- these first two lines are required
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # your stuff goes here
        self.titlelabel = tk.Label(self, text=name, font=controller.title_font)

        self.keybox = tk.Entry(self)
        self.keybox.insert(tk.INSERT, hex(self.key))
        self.keylabel = tk.Label(self, text="Key")
        # feedback is only needed for LFSR
        self.feedbackbox = tk.Entry(self)
        self.feedbackbox.insert(tk.INSERT, hex(self.feedback))
        self.feedbacklabel = tk.Label(self, text="Feedback")

        self.descriptionlabel = tk.Label(self, text=description, justify="left")

        self.inputbox = tk.Text(self, height=5, width=100)
        self.inputlabel = tk.Label(self, text="Input")
        self.outputbox = tk.Text(self, height=5, width=100)
        self.outputlabel = tk.Label(self, text="Output")

        self.openbutton = tk.Button(self, text="Open", command = self.clickedOpen)
        self.savebutton = tk.Button(self, text="Save", command = self.clickedSave)
        self.clearbutton = tk.Button(self, text="Clear Fields", command = self.clickedClear)
        self.encryptbutton = tk.Button(self, text="Encrypt/Decrypt", command = self.clickedEncrypt)
        # this uses a lambda because it has an argument
        # idk this is just what stackoverflow did
        self.backbutton = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        
        self.backbutton.grid(column = 0, row = 0)
        self.titlelabel.grid(column = 1, row = 0, columnspan=2)

        self.keylabel.grid(column = 0, row = 1)
        self.keybox.grid(column=1, row=1)
        self.feedbacklabel.grid(column=0, row=2)
        self.feedbackbox.grid(column=1, row=2)

        self.descriptionlabel.grid(column=2, row=1, rowspan=2)
        
        self.openbutton.grid(column=0, row=3)
        self.inputbox.grid(column=1, row=3, columnspan=2, rowspan=2)
        self.inputlabel.grid(column=0, row=4)

        self.savebutton.grid(column=0, row=5)
        self.outputbox.grid(column=1, row=5, columnspan=2, rowspan=2)
        self.outputlabel.grid(column=0, row=6)

        self.clearbutton.grid(column=1, row=7)
        self.encryptbutton.grid(column=2, row=7)

    def clickedEncrypt(self):
        try:
            self.key = int(self.keybox.get(), 16)
        except:
            messagebox.showerror(title="Key Error", message="Could not convert " + self.keybox.get() + " to hexadecimal. Please use a format like 0x1234ABCD.")
        
        try:
            self.feedback = int(self.feedbackbox.get(), 16)
        except:
            messagebox.showerror(title="Feedback Error", message="Could not convert " + self.feedbackbox.get() + " to hexadecimal. Please use a format like 0x1234ABCD.")

        if not self.usefileinput:
            self.input = self.inputbox.get(1.0, tk.END)
            self.input = codecs.escape_decode(self.input.encode('utf-8'))[0].decode("utf-8")

        self.output = crypt(self.input, self.key, self.feedback)
        self.outputbox.delete(1.0, tk.END)
        self.outputbox.insert(1.0, str(self.output)[12:-2])
        return
    
    def clickedClear(self):
        # TODO: clear key/feedback/input/output
        self.keybox.delete(0, tk.END)
        self.feedbackbox.delete(0, tk.END)
        # the text box widgets have a slightly different clearing method than the one-line entry widgets
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
        self.inputbox.config(state="disabled")
        return
    
    def clickedSave(self):
        # TODO: open file save dialogue
        file = filedialog.asksaveasfile(mode='wb')
        file.write(self.output)
        file.close()
        return