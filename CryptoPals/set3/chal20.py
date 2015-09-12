from set3_common import *

def challenge_20(plaintexts):
    global key

    key = gen_aes_key()
    nonce = 0
    enc_plaintexts = []
    for text in plaintexts:
        enc_plaintexts.append(ctr_cipher(key, nonce, text))

    longest = 0
    for enc in enc_plaintexts:
        if len(enc) > longest:
            longest = len(enc)

    blocks = ["" for _ in range(longest)]
    for enc in enc_plaintexts:
        for n, c in enumerate(enc):
            blocks[n] += c

    master_key = ""
    for block in blocks:
        score, key = single_byte_decrypt(block)
        master_key += chr(key)

    for enc in enc_plaintexts:
        print xor(enc, master_key)

if __name__ == "__main__":
    with open("20.txt", "r") as f:
        challenge_20([x.decode("base64") for x in f.readlines()])
