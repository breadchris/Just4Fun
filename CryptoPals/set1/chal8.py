from set1_common import *


def similar_blocks(text):
    block_size = 16
    blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]
    return len(set(blocks)) != len(blocks)

def challenge_8(data):
    lines = [str(n) for n, line in enumerate(data) if similar_blocks(line)]
    return lines

if __name__ == "__main__":
    with open("8.txt", "r") as f:
        data = []
        for line in f:
            data.append(line.strip().decode("hex"))
        print "[+] Output: %s" % ", ".join(challenge_8(data))
