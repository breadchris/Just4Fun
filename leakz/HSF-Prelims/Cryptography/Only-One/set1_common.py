import string

MIN_KEYSIZE = 2
MAX_KEYSIZE = 40
KEYSIZE_BLOCKS = 16
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
        elif x not in string.printable:
            deltas_sum += 0.05

    for c in freq_lookup:
        deltas_sum += abs((freq_lookup[c] / float(len(text))) - letterFreq[ord(c) - ord("A")])
    return deltas_sum

def single_byte_decrypt(encrypted_text):
    (sscore, skey) = (0, 0)
    for key in range(0, 255):
        decrypted_text = keyed_xor(encrypted_text, chr(key))
        print key, decrypted_text
        score = score_text(decrypted_text)
        if not sscore or (score != -1 and score < sscore):
            (sscore, skey) = (score, key)
    return sscore, skey
