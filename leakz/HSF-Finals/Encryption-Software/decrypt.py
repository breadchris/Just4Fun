from itertools import cycle, izip
import sys, magic
take = lambda itr, n: [x for y,x in zip(range(n), itr)]

# we can tell by looking at the output of next_cipher that it's a PRNG with a really small cycle... so here's the cycle
els = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,6,10,30,34,102,170,254,2,6,10,30,34,102,170,254,2,6,10,30,34,102,170,254]
# repeat it forever, n times (since we need to try all starting points of the cycle)
cycles = [cycle(els) for _ in els]
# Pop off first n elements for each nth cycle
for x in range(len(els)):
    take(cycles[x], x)

with open('enc') as f:
    plain = f.read()

# brute force against the 64 possible combinations, using UNIX file to check if it decodes as an MPEG v4
# We could check manually for the 'mp4' section in the header but this is nice and clean regardless.
print 'cracking...'
n_res = 0
for possibility in [izip(plain, cycle) for cycle in cycles]:
    possibility = ''.join([chr(ord(a) ^ b) for a,b in possibility]) 
    # if we have a match, write it out to a file (we may get multiple matches, but only one will actually make sense as a video, so we leave it to the user to go through them)
    if 'ISO Media, MP4 v2 [ISO 14496-14]' == magic.from_buffer(possibility):
        fname = '%d.mp4'%n_res
        n_res += 1
        with open(fname, 'w') as f:
            f.write(possibility)
        print "Wrote a possible result into " + fname
print "Check the possible results I wrote out with your favorite video viewer! :)"

