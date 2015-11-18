import base64

encoded = [s.strip() for s in open("release.txt", "r").readlines()]

flag = []
flag.append(base64.b64decode(encoded[0]).decode("UTF-8"))
flag.append(bytes.fromhex(encoded[1]).decode("UTF-8"))
flag.append("".join([chr(int(c, 10)) for c in encoded[2].split(" ")]))
flag.append("".join([chr(int(encoded[3][i:i+8], 2)) for i in range(0, len(encoded[3]), 8)]))
flag.append(base64.b32decode(encoded[4]).decode("UTF-8"))
print("".join(flag))

# the last part is ascii85 which they can decode online
# ex. https://www.tools4noobs.com/online_tools/ascii85_decode/
flag.append("it_was_numb3r_un0_y0}")

print("".join(flag))
