import re, random
text = file("alice.txt", "r").read()

tmp = [[[x.split(" ") for x in b] for b in _.split(". ") if b] for _ in [a for a in text.split("\n\n") if a]]

def find_char(c, t):
    if type(t) == str:
        print t
        if c == t:
            yield []
        else:
            yield False
    else:
        for n, a in enumerate(t):
            for x in find_char(c, a):
                if x:
                    x.insert(0, n + 1)
                    yield x

flag = ["all", "these", "fancy", "little", "things", "that", "Alice", "has"]
flag_numbers = []

for c in flag:
    print c
    flag_numbers.append(random.choice([x for x in find_char(c, tmp)]))

with file("lol_numbers.txt", "w") as f:
	for fa in flag_numbers:
		f.write(str(fa) + ", ")

