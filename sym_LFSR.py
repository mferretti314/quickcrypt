import tkinter as tk
from tkinter import messagebox

name = "LFSR"

description = """A Linear-Feedback Shift Register (LFSR) uses repeated bit shifts and XORs to encrypt data.
Security: Medium. Not incredibly cryptographically secure, but it's tricky to break in practice.
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

        self.input = ""
        self.inputinfo = """Type text here, or select "Open" to choose an input file."""
        self.output = ""
        self.outputinfo = """Click "Save" to save this output to a file."""

        # gui setup- these first two lines are required
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # your stuff goes here
        titlelabel = tk.Label(self, text=name, font=controller.title_font)

        keybox = tk.Entry(self)
        keylabel = tk.Label(self, text="Key")
        # feedback is only needed for LFSR
        feedbackbox = tk.Entry(self)
        feedbacklabel = tk.Label(self, text="Feedback")

        descriptionlabel = tk.Label(self, text=description, justify="left")

        inputbox = tk.Text(self, height=5, width=100)
        inputlabel = tk.Label(self, text="Input")
        outputbox = tk.Text(self, height=5, width=100)
        outputlabel = tk.Label(self, text="Output")

        openbutton = tk.Button(self, text="Open", command = self.clickedOpen)
        savebutton = tk.Button(self, text="Save", command = self.clickedSave)
        clearbutton = tk.Button(self, text="Clear Fields", command = self.clickedClear)
        encryptbutton = tk.Button(self, text="Encrypt/Decrypt", command = self.clickedEncrypt)
        # this uses a lambda because it has an argument
        # idk this is just what stackoverflow did
        backbutton = tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage"))
        
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
        if self.key == 0x00000000:
            messagebox.showerror(title="Error", message="No key set!")
            return
        if self.feedback == 0x00000000:
            messagebox.showerror(title="Error", message="No feedback set!")
            return
        
        byteinput = bytearray(self.input)
        self.output = crypt(byteinput, self.key, self.feedback)
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