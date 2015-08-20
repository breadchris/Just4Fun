from set2_common import *
from Crypto.Cipher import AES
from random import randint
from chal12 import decrypt_block
import string

secret = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""".replace("\n", "").decode("base64")

key = ""
random_bytes = "".join([chr(randint(0, 255)) for _ in range(randint(4, 5))])

def aes_encrypt_chal14(data):
    global key, random_bytes

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pkcs7_padding(random_bytes + data + secret, len(key))
    #print break_into_blocks(plaintext, len(key))

    encrypt = cipher.encrypt(plaintext)
    return encrypt

'''
This was a solution i was building out when i thought the random bytes
were generated for every encrypt call. The idea was to generate a string
that would allow you to find a known encrypted block in the encrypted output
and then from there look at the following block to correlate a byte with pkcs7
padding plaintext to an encrypted block.

def decrypt_secret(block_size):
    find_block = "A" * block_size * 3
    enc = aes_encrypt_chal14(find_block)
    search_block = similar_blocks(enc)[0]

    print "[+] Found search block:", repr(search_block)

    adjust_str = ""
    for i in range(block_size - 1):
        index = i + 1
        adjust_str += "B" * (block_size - i)
        adjust_str += "A" * block_size
        adjust_str += pkcs7_padding("x", block_size).replace("x", "{0}")
'''

def find_pad(block_size):
    init_pad = ""
    enc_length = len(aes_encrypt_chal14(init_pad))
    pad_length = 0
    for pad in range(block_size * 2):
        if enc_length != len(aes_encrypt_chal14(init_pad + "A" * pad)):
            init_pad += "A" * (pad - 1)
            break

    return init_pad

def decrypt_secret(block_size):
    init_pad = find_pad(block_size)
    enc = aes_encrypt_chal14("A" * block_size * 3)
    search_block = similar_blocks(enc, block_size)[0]
    offset = enc.find(search_block)
    replace_pad = ""
    secret_size = len(enc) - offset

    for i in range(block_size * 2):
        test = init_pad + "A" * i
        enc_test = aes_encrypt_chal14(test)
        if search_block in enc_test:
            replace_pad = test[:len(test) - block_size]
            break

    decrypt_secret = ""
    for block_off in range(0, secret_size, block_size):
        decrypt_secret = decrypt_block(
            block_size, offset + block_off, decrypt_secret,
            aes_encrypt_chal14, replace_pad)

    return decrypt_secret

def challenge_12():
    global key

    key = gen_aes_key()
    if not detect_ecb(aes_encrypt_chal14):
        print "[-] Error: Cipher not ECB"
        return

    block_size = find_block_size(aes_encrypt_chal14)
    if block_size == -1:
        print "[-] Error: Unable to determine block size"
        return

    print "[+] Found block size:", block_size
    print decrypt_secret(block_size)

if __name__ == "__main__":
    challenge_12()
