from set2_common import *
from Crypto.Cipher import AES
from random import randint
import string

secret = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""".replace("\n", "").decode("base64")

key = ""
random_bytes = "".join([chr(randint(0, 255)) for _ in range(randint(0, 150))])

def aes_encrypt(data):
    global key, random_bytes

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pkcs7_padding(random_bytes + data + secret, len(key))
    print break_into_blocks(plaintext, len(key))

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
    enc = aes_encrypt(find_block)
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
    enc_length = len(aes_encrypt(init_pad))
    pad_length = 0
    for pad in range(block_size):
        if enc_length != len(aes_encrypt(init_pad + "A" * pad)):
            init_pad += "A" * (pad - 1)
            break

    return init_pad

def decrypt_secret(block_size):
    init_pad = find_pad(block_size)
    enc = aes_encrypt("A" * block_size * 3)
    search_block = similar_blocks(enc, block_size)
    offset = enc.find(search_block)

    secret = ""
    for pad in range(block_size):
        cur_pad = init_pad + "A" * pad
        lookup = []
        for c in string.printable:
            test_pad = cur_pad + pkcs7_padding(secret + c)
            enc_block = aes_encrypt(test_pad)[offset:offset+block_size]
            lookup.append((enc_block, c))
        enc = aes_encrypt(init_pad)


def challenge_12():
    global key

    key = gen_aes_key()
    if not detect_ecb(aes_encrypt):
        print "[-] Error: Cipher not ECB"
        return

    block_size = find_block_size(aes_encrypt)
    if block_size == -1:
        print "[-] Error: Unable to determine block size"
        return

    print "[+] Found block size:", block_size
    print decrypt_secret(block_size)

if __name__ == "__main__":
    challenge_12()
