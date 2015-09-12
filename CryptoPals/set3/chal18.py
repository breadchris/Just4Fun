from set3_common import *

secret = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==".decode("base64")

def challenge_18():
    global secret

    key = "YELLOW SUBMARINE"
    nonce = 0
    decrypt = ctr_cipher(key, nonce, secret)

    print decrypt

if __name__ == "__main__":
    challenge_18()
