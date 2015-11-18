def keyed_xor(text, xor_key):
    return "".join([chr(ord(x) ^ ord(y) ^ (n % 255)) for n, (x, y) in enumerate(zip(text, xor_key * (len(text) / len(xor_key))))])

base = file("base.php", "r").read()
obfuscated = file("obfuscated.php", "r").read()

order = [238, 103, 16, 179, 227, 82, 86, 115, 22, 57, 210, 73, 155, 215, 175, 3, 165, 255, 49, 47]

for o in order:
    obfuscated = keyed_xor(obfuscated, chr(o))
    obfuscated += base

with open("release.php", "wb") as f:
    f.write(obfuscated)

# verify
for o in order[::-1]:
    obfuscated = keyed_xor(obfuscated, chr(o))

print obfuscated
if "THANK YOU" in obfuscated:
    print "yup good"

