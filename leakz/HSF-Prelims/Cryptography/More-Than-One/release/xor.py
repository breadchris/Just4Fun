import sys, os

#key: r1ckAstl3y1sb4e

def fun_function(text, xor_key):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(text, xor_key * (len(text) / len(xor_key)))])

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            return f.read().strip()
    else:
        raise Exception("File: %s does not exist" % filename)

def main(argv):
    if len(argv) != 5:
        print "Usage: %s ([encrypt] [decrypt]) [in] [out] [xor key]" % argv[0]
        sys.exit(1)

    xor_key = argv[4]
    in_data = read_file(argv[2])

    if argv[1] == "decrypt":
        print "[*] Decrypting file with xor key:", xor_key
        with open(argv[3], "w") as out:
            out.write(fun_function(in_data, xor_key))
        print "[+] Decryption Finished"
    elif argv[1] == "encrypt":
        print "[*] Encrypting file with xor key:", xor_key
        with open(argv[3], "w") as out:
            out.write(fun_function(in_data, xor_key))
        print "[+] Encryption Finished"

if __name__ == "__main__":
    main(sys.argv)
