from set3_common import *

def challenge_21():
    twister = MT19937(1337)
    for n in range(256):
        print "[+] Random number ({0}):{1}".format(n, twister.extract_number())

if __name__ == "__main__":
    challenge_21()
