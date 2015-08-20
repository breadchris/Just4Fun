
def keyed_xor(text, xor_key):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(text, xor_key * (len(text) / len(xor_key)))])

def challenge_5(text, key):
    return keyed_xor(text, key)

if __name__ == "__main__":
    '''
    text = raw_input("[?] Text: ")
    key  = raw_input("[?] Key: ")
    '''

    text = '''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal
'''
    key = "ICE"

    print "[+] Output: %s" % challenge_5(text, key).encode("hex")
