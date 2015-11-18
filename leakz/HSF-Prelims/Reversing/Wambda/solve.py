
switches = []
with open("switches.txt", "r") as f:
    switches = [eval(_.strip()) for _ in f.readlines()]

out = ""
with open("out.txt", "r") as f:
    out = list(eval(f.read().strip()))

for s in switches:
    tmp = out[s[1]]
    out[s[1]] = out[s[0]]
    out[s[0]] = tmp

print out

