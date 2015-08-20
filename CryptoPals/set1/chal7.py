from Crypto.Cipher import AES


def challenge_7(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

if __name__ == "__main__":
    with open("7.txt", "rb") as f:
        data = f.read().decode("base64")
        key = "YELLOW SUBMARINE"
        print "[+] Output: %s" % challenge_7(data, key)
