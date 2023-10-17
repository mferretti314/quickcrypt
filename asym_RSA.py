# very wip. 

class asym_RSA():
    
    def __init__(self):
        self.privateKey = "private"
        self.publicKey = "public"
        self.data = "data"

    # returns a string that describes the algorithm.
    def getDescription(self):
        return """An asymmetric encryption algorithm. This implementation is RSA PKCS#1 OAEP (Optimal Asymmetric Encryption Padding). 
    The RSA algorithm is used to generate and share a private key, which is then used to encrypt data via AES.
    Requires the reciever's public_key (file or text), and your own private_key (file or text). 
    The message will be secure even if the reciever sends their public key on an unsecure channel."""


    # Generates a keypair and saves both the public and private keys to a file.
    def genKeyPair(self):
        self.privateKey = "new private key"
        self.publicKey = "new public key"
        print("Stub method for key generation.")
        return (self.publicKey, self.privateKey)
    
    # Called when the user hits the "load private key" button
    def loadSender(self):
        print("Stub method for loading key")

    # Called when the user hits the "load public key" button
    def loadReciever(self):
        print("Stub method for loading key")
