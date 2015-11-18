from set1_common import *
import string

def challenge_4(encrypted_line):
    hline = ""
    hscore = 0
    line = encrypted_line
    score, key= single_byte_decrypt(line)

    (hscore, hline) = (score, keyed_xor(line, chr(key)))
    if hscore == 0 or (score != 0 and score < hscore):
        (hscore, hline) = (score, keyed_xor(line, chr(key)))
    return hline

if __name__ == "__main__":
    with open("encrypt.txt", "r") as f:
        print "[+] Output: %s" % repr(challenge_4(f.read().strip().decode("hex")))
