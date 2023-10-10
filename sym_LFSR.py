class sym_LFSR:
    key = 0x12345678
    feedback = 0x87654321
    data = "data to encrypt/decrypt"
    description = """Linear-Feedback Shift Register (LFSR) is a cipher that uses repeated bit shifts and XORs to encrypt data. It's also used to generate random numbers.
    It isn't the most secure algorithm, but it's still difficult to break, especially for shorter messages without known plaintext."""
    
    def crypt(key):
        tempkey = key
        shift(tempkey)


    def shift(tempkey):
        for x in range(0,8):
            tempkey = minishift(tempkey)
        return tempkey
        
    def minishift(tempkey):
        if (tempkey & 1 == 1):
            return (tempkey >> 1)
        else:
            return (tempkey >> 1) ^ feedback