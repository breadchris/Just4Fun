
solve = True

if not solve:
    s = ""
    with open("flag.png", "rb") as f:
        s = f.read()

    out = ""
    for c in s:
        if ord(c) == ord("G"):
            out += "\x39"
        else:
            out += c

    with open("release.png", "wb") as a:
        a.write(out)
else:
    s = ""
    with open("release.png", "rb") as f:
        s = f.read()

    out = ""
    for c in s:
        if ord(c) == ord("\x39"):
            out += "G"
        else:
            out += c

    with open("solve.png", "wb") as a:
        a.write(out)

