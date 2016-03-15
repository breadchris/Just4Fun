from set1_common import *

def get_key_size(text):
    skey = 2
    sdistance = -1
    for key_size in range(MIN_KEYSIZE, MAX_KEYSIZE):
        distance = edit_distance(text, key_size) / key_size
        if sdistance < 0 or distance < sdistance:
            sdistance = distance
            skey = key_size
    return skey

def challenge_6(data):
    key_size = get_key_size(data)
    blocks = ["" for _ in range(key_size)]
    for n, x in enumerate(data):
        blocks[n % key_size] += x

    key = ""
    for n, block in enumerate(blocks):
        score, key_char = single_byte_decrypt(block)
        key += chr(key_char)
    print "[+] Found the key:", repr(key)

    return keyed_xor(data, key)

if __name__ == "__main__":
    with open("AncientSecretsOfTheKamaSutra.txt", "r") as f:
        data = f.read()
        print "[+] Output:", challenge_6(data)

