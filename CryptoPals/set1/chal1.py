def challenge_1(user_input):
    return user_input.decode("hex").encode("base64", "strict")

if __name__ == "__main__":
    user_input = raw_input("[?] Hex encoded string: ")

    print "[+] Output: %s" % challenge_1(user_input)

