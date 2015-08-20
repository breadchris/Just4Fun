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
    blocks = [""] * key_size
    for n, x in enumerate(data):
        blocks[n % key_size] += x
    
    key = [None] * key_size
    for n, block in enumerate(blocks):
        key[n] = chr(single_byte_decrypt(block)[1])
    print "".join(key)

    return keyed_xor(data, "".join(key))

if __name__ == "__main__":
    with open("in.txt", "r") as f:
        data = f.read().replace("\n", "").decode("hex")#.decode("base64")
        print "[+] Output: %s" % challenge_6(data)

