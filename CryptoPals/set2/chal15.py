from set2_common import *

def challenge_15():
    block_size = 16

    valid   = "FunFunFunFun\x04\x04\x04\x04"
    invalid = "FunFunFunFun\x04\x05\x04\x04"

    try:
        print pkcs7_unpad(valid, block_size)
    except PKCS7PaddingError as e:
        print e

    try:
        print pkcs7_unpad(invalid, block_size)
    except PKCS7PaddingError as e:
        print e

if __name__ == "__main__":
    challenge_15()
