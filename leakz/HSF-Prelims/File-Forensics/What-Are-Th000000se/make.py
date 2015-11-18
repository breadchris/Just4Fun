
import md5, random

flag = ["flag{", "h", "/-\\", "s", "h", "_", "i", "t", "_", "o", "u", "t", "}"]
hint = ["I", "have", "heard", "md5", "only", "has", "hex", "chars"]

hint_stuff = []
for h in hint:
    hint_stuff.append(md5.new(h).hexdigest())
print hint_stuff

words = [x.strip() for x in file("words", "r").readlines()]
random.shuffle(words)
words_len = 6969 - len(hint_stuff)
hash_places = random.sample(range(len(hint_stuff), words_len), len(flag))
freq = 10
cur_char = 0


with open("hashes.md5", "w") as f:
    for h in hint_stuff:
        f.write(h + "\n")
    for i in range(words_len):
        h = md5.new(words[i]).hexdigest()
        if i in hash_places:
            idx = random.randint(0, len(h) - len(flag[cur_char]))
            for n, c in enumerate(flag[cur_char]):
                h = h[:idx + n - 1] + flag[cur_char][n] + h[idx + n:]
            if len(h) > 32:
                h = h[:-len(flag[cur_char])]
            cur_char += 1
        f.write(h + "\n")

def solve():
    flag = ""
    with open("hashes.md5", "r") as f:
        for line in f.readlines():
            for c in line.strip():
                if c not in "0123456789abcdef":
                    flag += c

    print flag

solve()
