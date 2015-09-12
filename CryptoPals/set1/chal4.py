from set1_common import *
import string

def challenge_4(encrypted_lines):
    hline = ""
    hscore = 0
    for line in encrypted_lines:
        line = line.strip().decode("hex")
        score, key= single_byte_decrypt(line)

        if hscore == 0 or (score != 0 and score < hscore):
            (hscore, hline) = (score, keyed_xor(line, chr(key)))
    return hline

if __name__ == "__main__":
    with open("4.txt", "r") as f:
        print "[+] Output: %s" % repr(challenge_4(f))
