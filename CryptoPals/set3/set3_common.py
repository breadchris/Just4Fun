from random import *
from Crypto.Cipher import AES
from struct import pack

def ctr_cipher(key, nonce, data):
    cipher = AES.new(key)

    blocks = break_into_blocks(data)
    decrypt_out = ""
    for n, block in enumerate(blocks):
        ctr_block = pack("<QQ", nonce, n)
        enc_ctr = cipher.encrypt(ctr_block)
        decrypt_out += xor(block, enc_ctr)
    return decrypt_out

class PKCS7PaddingError(Exception):
    def __init__(self, message, data):
        super(PKCS7PaddingError, self).__init__(message)
        self.data = data

    def __str__(self):
        return self.message + ": " + repr(self.data)

def pkcs7_padding(text, block_size=16):
    pad = len(text) % block_size
    if pad == 0:
        return text
    pad = block_size - pad
    return text + (chr(pad) * pad)

def pkcs7_unpad(text, block_size=16):
    pad = ord(text[-1])
    if pad > block_size:
        raise PKCS7PaddingError("Given padding is not valid", text)

    pad_chars = text[-pad:]
    if (len(pad_chars) == 1 and ord(pad_chars[0]) == 0x01) or \
        all([pad_chars[0] == c for c in pad_chars[1:]]):
        return text[:-pad]
    else:
        raise PKCS7PaddingError("Given padding is not valid", text)

def gen_aes_key(length=16):
    return "".join([chr(randint(0, 255)) for _ in range(length)])

def break_into_blocks(text, block_size=16):
    return [text[i:i + block_size] for i in range(0, len(text), block_size)]

def xor(text, xor_key):
    out = ""
    for n, c in enumerate(text):
        out += chr(ord(c) ^ ord(xor_key[n % len(xor_key)]))
    return out

letterFreq = [0.0816, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
              0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
              0.07507, 0.01929, 0.00095, 0.05987, 0.06326, 0.09055, 0.02758,
              0.00978, 0.0236, 0.0015, 0.01974, 0.00074]

def keyed_xor(text, xor_key):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(text, xor_key * (len(text) / len(xor_key)))])

def edit_distance(text, size):
    total_sum = 0
    blocks = [text[s:s + size] for s in range(0, size * KEYSIZE_BLOCKS, size)]
    for text1, text2 in zip(*[iter(blocks)]*2):
        total_sum += sum([bin(ord(x) ^ ord(y)).count("1") for x, y in zip(text1, text2)])
    return total_sum

def score_text(text):
    deltas_sum = 0
    freq_lookup = {chr(c):0 for c in range(ord("A"), ord("Z") + 1)}
    for x in text.upper():
        if x.isalpha():
            freq_lookup[x] += 1
        elif x not in " '\"":
            deltas_sum += 0.05

    for c in freq_lookup:
        deltas_sum += abs((freq_lookup[c] / float(len(text))) - letterFreq[ord(c) - ord("A")])
    return deltas_sum

def single_byte_decrypt(encrypted_text):
    (sscore, skey) = (0, 0)
    for key in range(0, 255):
        decrypted_text = keyed_xor(encrypted_text, chr(key))
        score = score_text(decrypted_text)
        if not sscore or (score != -1 and score < sscore):
            (sscore, skey) = (score, key)
    return sscore, skey


# Taken from: https://en.wikipedia.org/wiki/Mersenne_Twister
def _int32(x):
    # Get the 32 least significant bits.
    return int(0xFFFFFFFF & x)

class MT19937:

    def __init__(self, seed):
        # Initialize the index to 0
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = seed  # Initialize the initial state to the seed
        for i in range(1, 624):
            self.mt[i] = _int32(
                1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def extract_number(self):
        if self.index >= 624:
            self.twist()

        y = self.mt[self.index]

        print "[0]", y
        # Right shift by 11 bits
        y = y ^ y >> 11
        print "[1]", y
        # Shift y left by 7 and take the bitwise and of 2636928640
        y = y ^ y << 7 & 2636928640
        print "[2]", y
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ y << 15 & 4022730752
        print "[3]", y
        # Right shift by 18 bits
        y = y ^ y >> 18
        print "[4]", y

        self.index = self.index + 1

        return _int32(y)

    def twist(self):
        for i in range(0, 624):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            y = _int32((self.mt[i] & 0x80000000) +
                       (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0
