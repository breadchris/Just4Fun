from Crypto.Cipher import AES


def keyed_xor(text, xor_key):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(text, xor_key * (len(text) / len(xor_key)))])

def ecb_decrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

def cbc_decrypt(key, IV, data):
    blocks = [data[i:i + len(key)] for i in range(0, len(data), len(key))]
    prev_block = IV
    decrypt_blocks = []

    for block in blocks:
        decrypt_block = ecb_decrypt(key, block)
        combine = keyed_xor(prev_block, decrypt_block)
        decrypt_blocks.append(combine)
        prev_block = block

    print decrypt_blocks
    return "".join(decrypt_blocks)

def challenge_10(key, IV, data):
    decrypted = cbc_decrypt(key, IV, data)
    return decrypted

if __name__ == "__main__":
    key = "YELLOW SUBMARINE"
    IV = "\x00" * len(key)
    enc_file = "chal10.txt"
    enc_out_file = "chal10.out"

    decrypted = ""
    with open(enc_file, "rb") as enc:
        data = enc.read().replace("\n", "").decode("base64")
        decrypted = challenge_10(key, IV, data)

    with open(enc_out_file, "wb") as out:
        out.write(decrypted)
