
flag = list("NO FLAG FOR YOU")

def sort(s):
    for i in range(len(s)):
        h = i
        for j in range(i, len(s)):
            h = j if ord(s[j]) > ord(s[h]) else h
        t = s[i]
        s[i] = s[h]
        s[h] = t

sort(flag)
print(flag)

