import string

nonmd5 = string.maketrans(string.hexdigits, ' ' * len(string.hexdigits))

i = open('hashes.md5', 'r').read().strip().split('\n')

o = [''.join([a.translate(nonmd5).strip() for a in i])]

print o


