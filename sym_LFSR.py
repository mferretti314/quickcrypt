description = """Linear-Feedback Shift Register (LFSR) is a cipher that uses repeated bit shifts and XORs to encrypt data. It's also used to generate random numbers.
It isn't the most secure algorithm, but it's still difficult to break, especially for shorter messages without known plaintext.
Notably, it is symmetrically reversible, which means you do the same operations to encrypt data as you do to decrypt it."""

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