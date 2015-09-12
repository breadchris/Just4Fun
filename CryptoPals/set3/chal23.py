from set3_common import *
import time

def verify(rand1, rand2):
    for _ in range(10000):
        assert rand1.extract_number() == rand2.extract_number()

def untamper(rand_int):
    ''' Original operations
    y = y ^ y >> 11
    y = y ^ y << 7 & 2636928640
    xxxxxxxxxxxxxxxxxxxxxxxxxkkkkkkk
    xxxxxxxxxxxxxxxxxxkkkkkkk0000000
    10011101001011000101011010000000
    000000000000000000kkkkkkkkkkkkkk
    y = y ^ y << 15 & 4022730752
    y = y ^ y >> 18
    '''
    print "AAAAAAAAAAAAAAAAAA"
    print "[4]", rand_int
    rand_int = rand_int ^ rand_int >> 18
    print "[3]", rand_int
    rand_int = rand_int ^ rand_int << 15 & 4022730752
    print "[2]", rand_int

    out = rand_int & (2**8 - 1)
    for i in range(4):
        out_part = out & ((2**8 - 1) << (7 * i))
        part = rand_int ^ out_part << 7 & 2636928640
        out &= part & ((2**8 - 1) << (7 * (i + 1)))

    rand_int = out

    # rand_int = rand_int ^ rand_int << 7 & 2636928640
    print "[1]", rand_int
    rand_int = rand_int ^ rand_int >> 11
    print "[0]", rand_int

    return rand_int

def challenge_23():
    start_time = 0xFFFFFFFF & int(time.time())
    rand = MT19937(start_time)

    rand_int = rand.extract_number()
    print untamper(rand_int)

if __name__ == "__main__":
    challenge_23()
