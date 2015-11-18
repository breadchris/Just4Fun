
with open("morse.txt", "r") as f:
    with open("doots.txt", "w") as g:
        g.write(f.read().replace(".", "doot").replace("-", "doooot"))
