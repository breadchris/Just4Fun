from set2_common import *
from Crypto.Cipher import AES
import string


secret = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""".replace("\n", "").decode("base64")

key = ""

def aes_encrypt(data):
    global key

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pkcs7_padding(data + secret, len(key))
    return cipher.encrypt(plaintext)

def decrypt_block(block_size, off=0, secret_part="", cipher=aes_encrypt, bp=""):
    decrypt_out = secret_part
    for pad in range(block_size)[::-1]:
        base_pad = bp + pad * "A"
        base = base_pad + decrypt_out + "{0}"
        lookup = []
        tmp = []
        for c in range(255):
            to_encrypt = base.format(chr(c))
            enc = cipher(to_encrypt)
            lookup.append((enc[off:off+block_size], chr(c)))
        enc = cipher(base_pad)
        find_block = enc[off:off+block_size]
        for t in lookup:
            if t[0] == find_block:
                decrypt_out += t[1]
                break
    return decrypt_out

def decrypt_secret(block_size):
    secret_size = len(aes_encrypt("A" * block_size)) - block_size
    decrypt_secret = ""
    for block_off in range(0, secret_size, block_size):
        decrypt_secret = decrypt_block(block_size, block_off, decrypt_secret)

    return decrypt_secret

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
