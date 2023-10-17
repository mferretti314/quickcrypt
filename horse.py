import random
import sys
import uuid


class horse:
    def __init__(self):
        self.horse_key = 0
    
    def get_description():
        return """Peter, the horse is here. https://www.youtube.com/watch?v=roi2cyto-yk
                  I will not be explaining my methods."""
    
    def gen_key(self):
        self.horse_key = random.randint(-sys.maxsize, sys.maxsize)
        with open(f"{str(uuid.uuid4())}.horse", 'w+') as horse_file:
            horse_file.write(str(self.horse_key))

    def load_key(self, file_name):
        with open(file_name) as horse_key:
            self.horse_key = int(horse_key.readline())

    def horse_crypt(self, file_name):
        random.seed(self.horse_key)
        with open(file_name, encoding='utf-8') as to_be_horsified, open(f"{file_name}.horse", 'w+', encoding='utf-8') as horse_crypted:
            for line in to_be_horsified:
                for char in line:
                    horse_offset = random.randint(0, sys.maxsize)
                    horse_crypted.write(''.join(['\U0001F40E' if x == "1" else u'\u2800' for x in str(bin(ord(char) + horse_offset))[2:]]) + '\n')

    def horse_decrypt(self, file_name):
        random.seed(self.horse_key)
        with open(file_name, encoding='utf-8') as unhorse, open(f"{file_name[:-6]}", 'w+', encoding='utf-8') as unencrypt:
            for line in unhorse:
                horse_offset = random.randint(0, sys.maxsize)
                unencrypt.write(chr(int(''.join(['1' if x == '\U0001F40E' else '0' for x in line[0:len(line)-1]]), 2) - horse_offset))

if __name__ == "__main__":
    horse_test = horse()
    horse_test.gen_key()
    horse_test.horse_crypt("dog.txt")
    horse_test.horse_decrypt("dog.txt.horse")