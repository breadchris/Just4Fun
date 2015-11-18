import sys, os

def fun_function(text, xor_key):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(text, xor_key * (len(text) / len(xor_key)))])

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            return f.read().strip()
    else:
        raise Exception("File: %s does not exist" % filename)

def main(argv):
    if len(argv) != 4:
        print "Usage: %s ([encrypt] [decrypt]) [filename] [xor key]" % argv[0]
        sys.exit(1)

    xor_key = argv[3]
    file_data = read_file(argv[2])

    if argv[1] == "decrypt":
        print "[*] Decrypting file with xor key:", repr(xor_key.decode("hex"))
        print fun_function(file_data.decode("hex"), xor_key.decode("hex"))
        print "[+] Decryption Finished"
    elif argv[1] == "encrypt":
        print "[*] Encrypting file with xor key:", repr(xor_key.decode("hex"))
        print fun_function(file_data, xor_key.decode("hex")).encode("hex")
        print "[+] Encryption Finished (data encoded in hexidecimal format)"

if __name__ == "__main__":
    main(sys.argv)
