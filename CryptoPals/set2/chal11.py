from set2_common import *
from Crypto.Cipher import AES


def encryption_oracle(data):
    bytes_before = "".join([chr(randint(0, 255)) for _ in range(randint(5, 10))])
    bytes_after  = "".join([chr(randint(0, 255)) for _ in range(randint(5, 10))])
    key = gen_aes_key()
    data = bytes_before + data + bytes_after
    data = pkcs7_padding(data, len(key))
    mode = randint(0, 1)
    if mode == 0:
        IV = gen_aes_key()
        cipher = AES.new(key, AES.MODE_CBC, IV)
        print "[*] Actual: CBC"
    else:
        cipher = AES.new(key, AES.MODE_ECB)
        print "[*] Actual: ECB"

    return cipher.encrypt(data)

def challenge_11(runs):
    for _ in range(runs):
        if detect_ecb(encryption_oracle):
            print "[+] Guess: ECB\n"
        else:
            print "[+] Guess: CBC\n"

if __name__ == "__main__":
    runs = 5
    challenge_11(5)
