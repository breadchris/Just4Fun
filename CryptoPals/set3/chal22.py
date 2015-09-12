from set3_common import *
from random import randint
from time import time
import time

def verify():
    rand_int = randint(0, 999999)
    rand1 = MT19937(rand_int)
    rand2 = MT19937(rand_int)
    for _ in range(10000):
        assert rand1.extract_number() == rand2.extract_number()

def challenge_22():
    verify()

    cur_time = time.time()
    delay1 = randint(40, 1000)
    delay2 = randint(40, 1000)

    # sleep(delay1)

    start_time = 0xFFFFFFFF & int(time.time())
    print "[*] Start time for first random generator is:", start_time
    rand = MT19937(start_time)
    first_rand = rand.extract_number()

    # sleep(delay2)

    cur_time = 0xFFFFFFFF & int(time.time())
    for i in range(9999):
        test_rand = MT19937(cur_time - i)
        if test_rand.extract_number() == first_rand:
            print "[+] Found time:", cur_time - i
            break

if __name__ == "__main__":
    challenge_22()
