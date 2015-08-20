import sys
from set2_common import *
from Crypto.Cipher import AES

key = ""
IV = ""

def aes_encrypt_chal16(data):
    global key

    cipher = AES.new(key, AES.MODE_CBC, IV)
    plaintext = pkcs7_padding(data, len(key))
    #print break_into_blocks(plaintext, len(key))

    encrypt = cipher.encrypt(plaintext)
    return encrypt

def aes_decrypt_chal16(data):
    global key

    cipher = AES.new(key, AES.MODE_CBC, IV)
    try:
        return cipher.decrypt(data)
    except:
        print "[-] Unable to decrypt data"
        sys.exit(8)

def format_input(data):
    prepend = "comment1=cooking%20MCs;userdata="
    append = ";comment2=%20like%20a%20pound%20of%20bacon"
    data = data.replace("=", "").replace(";", "")
    return aes_encrypt_chal16(pkcs7_padding(prepend + data + append))

def parse_input(data):
    decrypt = aes_decrypt_chal16(data)
    try:
        user_input = pkcs7_unpad(decrypt)
    except:
        return

    try:
        return user_input, {x[0]:x[1] for x in [y.split("=") for y in user_input.split(";")]}
    except:
        return user_input, {}

def challenge_16():
    global key, IV

    block_size = 16
    key = gen_aes_key()
    IV = gen_aes_key()

    target_block = ";user=admin;a=aa"

    enc = format_input("A" * block_size)
    blocks = break_into_blocks(enc)

    fake_block = ""
    for i in range(0, block_size):
        block_lookup = {}
        for c in range(255):
            blocks[2] = fake_block + "A" * (block_size - i - 1)
            blocks[2] = blocks[2][:i] + chr(c) + blocks[2][i:]
            user_input, out = parse_input("".join(blocks))
            test_blocks = break_into_blocks(user_input)
            block_lookup[chr(c)] = test_blocks[3][i]

        if target_block[i] in block_lookup:
            fake_block += block_lookup[target_block[i]]
        else:
            print "[-] Hay un problemo, no bit "

    blocks[2] = fake_block
    user_input, out = parse_input("".join(blocks))
    print repr(user_input)

    if "user" in out and out["user"] == "admin":
        print "[+] User is authed :D"
    else:
        print "[-] User is not 1337"

if __name__ == "__main__":
    challenge_16()
