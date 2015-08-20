from set2_common import *
from Crypto.Cipher import AES

key = ""

def aes_encrypt(data):
    global key

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = pkcs7_padding(data, len(key))
    return cipher.encrypt(plaintext)

def aes_decrypt(data):
    global key

    cipher = AES.new(key, AES.MODE_ECB)
    decrypt = cipher.decrypt(data)
    return pkcs7_unpad(decrypt, len(key))

def parse_params(s):
    return {k:v for k, v in [x.split("=") for x in s.split("&")]}

def profile_for(email):
    email = email.replace("=", "").replace("&", "")
    return "email={email}&uid={uid}&role={role}".format(
        email=email, uid=10, role="user")

def create_fake_email(block_size):
    email_str = "email="
    fake_email = "A" * (block_size - len(email_str))
    fake_email += pkcs7_padding("admin", block_size)
    return fake_email

def auth_loop():
    global key

    block_size = 16
    # Make plaintext look like (space indicates new block)
    # email=AAAAAAAAAA admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b &uid=10&role=use r\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf\x0xf
    email = create_fake_email(block_size)
    response = aes_encrypt(profile_for(email))

    # Take the resulting second block...
    admin_block = response[block_size:block_size * 2]

    # Coerce the "user" to be in the last block with the padding...
    email = "A" * (block_size - (len("email=&uid=10&role=") % block_size))
    response = aes_encrypt(profile_for(email))
    response = response[:-block_size] + admin_block

    try:
        decrypt_data = aes_decrypt(response)
        print "[+] Data decrypted: ", decrypt_data
    except:
        print "[-] Unable to decrypt request:", repr(response)
        return
    user = parse_params(decrypt_data)

    if user["role"] == "admin":
        print "[+] User is authed into system :D"
        print "[+] You are 1337 now"
    else:
        print "[-] User is not authed"

def challenge_13():
    global key

    key = gen_aes_key()
    auth_loop()

if __name__ == "__main__":
    challenge_13()
