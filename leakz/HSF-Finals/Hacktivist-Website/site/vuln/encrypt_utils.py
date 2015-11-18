from random import *
from Crypto.Cipher import AES
from struct import pack

def aes_encrypt():
    global key, random_string

    IV = gen_aes_key()

    cipher = AES.new(key, AES.MODE_CBC, IV)
    plaintext = pkcs7_padding(random_string, len(key))

    encrypt = cipher.encrypt(plaintext)
    return IV, encrypt

def aes_decrypt(IV, data):
    global key

    cipher = AES.new(key, AES.MODE_CBC, IV)
    try:
        decrypt = cipher.decrypt(data)
        pkcs7_unpad(decrypt, len(key))
        return True
    except:
        return False

class PKCS7PaddingError(Exception):
    def __init__(self, message, data):
        super(PKCS7PaddingError, self).__init__(message)
        self.data = data

    def __str__(self):
        return self.message + ": " + repr(self.data)

def pkcs7_padding(text, block_size=16):
    pad = len(text) % block_size
    if pad == 0:
        return text
    pad = block_size - pad
    return text + (chr(pad) * pad)

def pkcs7_unpad(text, block_size=16):
    pad = ord(text[-1])
    if pad > block_size:
        raise PKCS7PaddingError("Given padding is not valid", text)

    pad_chars = text[-pad:]
    if (len(pad_chars) == 1 and ord(pad_chars[0]) == 0x01) or \
        all([pad_chars[0] == c for c in pad_chars[1:]]):
        return text[:-pad]
    else:
        raise PKCS7PaddingError("Given padding is not valid", text)

def gen_aes_key(length=16):
    return "".join([chr(randint(0, 255)) for _ in range(length)])

def break_into_blocks(text, block_size=16):
    return [text[i:i + block_size] for i in range(0, len(text), block_size)]

