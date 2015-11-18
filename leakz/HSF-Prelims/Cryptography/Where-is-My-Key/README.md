
You are given the encryption program (encryptor.c) a plaintext file (message_1) and its associated encrypted file (message_1.enc)
you are also given an encrypted file (message_2.enc, which uses the same key as the first encrypted file) 

the goal is to decrypt message_2.enc

in order to do this, they must first reverse the encryption algorithm so that they figure out to take the first encrypted file and first plaintext file and work with them together to arrive at the encryption key (see decrypt.py for this).

Once you have the key, you can work backwards in a similar way to arrive at the plaintext for the second encrypted file to get the flag
