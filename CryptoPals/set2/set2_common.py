from random import randint

def pkcs7_padding(text, block_size):
    pad = len(text) % block_size
    if pad == 0:
        return text
    pad = block_size - pad
    return text + (chr(pad) * pad)

def pkcs7_unpad(text, block_size):
    pad = ord(text[-1])
    if pad >= block_size:
        print text
        return text
    return text[:-pad]

def gen_aes_key(length=16):
    return "".join([chr(randint(0, 255)) for _ in range(length)])

def break_into_blocks(text, block_size):
    return [text[i:i + block_size] for i in range(0, len(text), block_size)]

def similar_blocks(text, block_size=16):
    blocks = break_into_blocks(text, block_size)
    repeated_blocks = []
    for n, block1 in enumerate(blocks):
        for m, block2 in enumerate(blocks):
            if n != m and block1 == block2 and block1 not in repeated_blocks:
                repeated_blocks.append(block1)
    return repeated_blocks

def find_block_size(cipher):
    base_len = len(cipher("A"))
    block_length = 0
    for i in range(2, 512):
        test_len = len(cipher("A" * i))
        if test_len > base_len:
            if block_length:
                return block_length
            else:
                block_length = 1
                base_len = test_len
        elif block_length:
            block_length += 1

    return -1

def detect_ecb(cipher):
    break_str = "A"*16*3
    enc = cipher(break_str)
    return len(similar_blocks(enc)) > 0

def print_hex(h):
    print [hex(ord(c)) for c in h]
