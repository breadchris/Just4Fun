from set1_common import *

def challenge_3(encrypted):
    score, key = single_byte_decrypt(encrypted)
    return keyed_xor(encrypted, chr(key))

if __name__ == "__main__":
    ciphertext  = raw_input("[?] Ciphertext: ")

    print "[+] Output: %s" % challenge_3(ciphertext.decode("hex"))

