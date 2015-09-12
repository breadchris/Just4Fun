from set3_common import *
from Crypto.Cipher import AES
from random import *

random_string = choice([x.decode("base64") for x in """
MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93
"""[1:-1].split("\n")])

key = ""

def aes_encrypt_chal17():
    global key, random_string

    IV = gen_aes_key()

    cipher = AES.new(key, AES.MODE_CBC, IV)
    plaintext = pkcs7_padding(random_string, len(key))
    #print break_into_blocks(plaintext, len(key))

    encrypt = cipher.encrypt(plaintext)
    return IV, encrypt

def aes_decrypt_chal17(IV, data):
    global key

    cipher = AES.new(key, AES.MODE_CBC, IV)
    try:
        decrypt = cipher.decrypt(data)
        pkcs7_unpad(decrypt, len(key))
        return True
    except:
        return False

def challenge_17():
    global key

    key = gen_aes_key()

    IV, enc = aes_encrypt_chal17()

    blocks = break_into_blocks(enc)
    actual_iv = IV
    decrypt_out = ""
    for n, block in enumerate(blocks):
        decrypt_block = ""
        pad_block = ""
        for i in range(1, len(block) + 1):
            tmp_pad_block = "".join([chr(ord(x) ^ i) for x in pad_block])
            for c in range(255):
                test_iv = (chr(c) + tmp_pad_block).rjust(len(block), "\x00")
                if aes_decrypt_chal17(test_iv, block):
                    inter_byte = c ^ i
                    pad_block = chr(inter_byte) + pad_block
                    decrypt_byte = chr(inter_byte ^ ord(actual_iv[-i]))
                    decrypt_block = decrypt_byte + decrypt_block
                    break
        decrypt_out += decrypt_block
        actual_iv = block

    decrypt_out = pkcs7_unpad(decrypt_out)
    assert decrypt_out == random_string
    print "[+] Decrypted:", decrypt_out

if __name__ == "__main__":
    challenge_17()
