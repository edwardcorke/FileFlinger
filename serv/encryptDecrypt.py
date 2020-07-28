from cryptography.fernet import Fernet
import pathlib

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    filepath = str(pathlib.Path(__file__).parent.absolute()) + '\\key.key'
    return open(filepath, "rb").read()


def encrypt(file_data, key):
    f = Fernet(key)
    return f.encrypt(file_data)


def decrypt(file_data, key):
    f = Fernet(key)
    return f.decrypt(file_data)
