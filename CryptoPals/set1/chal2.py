
def challenge_2(plaintext, xor_key):
    return "".join([chr(ord(x)^ord(y))for x,y in zip(plaintext.decode("hex"), xor_key.decode("hex"))])

if __name__ == "__main__":
    plaintext  = raw_input("[?] Plaintext: ")
    xor_key = raw_input("[?] XOR Key: ")

    print "[+] Output: %s" % challenge_2(plaintext, xor_key).encode("hex")

