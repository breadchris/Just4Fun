from set1_common import *

def challenge_4(encrypted_lines):
    lline = ""
    lscore = 100000
    for line in encrypted_lines:
        score, key = single_byte_decrypt(line.strip().decode("hex"))
        if score < lscore:
            (lscore, lline) = (score, keyed_xor(line, key))
    return lline

if __name__ == "__main__":
    with open("4.txt", "r") as f:
        print "[+] Output: %s" % challenge_4(f)
