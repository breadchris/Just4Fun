
def challenge_9(text, block_size):
    pad = block_size - len(text)
    return text + (chr(pad) * pad)

if __name__ == "__main__":
    data = raw_input("Data: ")
    block_size = int(raw_input("Block Size: "))
    print "[+] Output: %s" % repr(challenge_9(data, block_size))
