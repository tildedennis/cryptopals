import base64
import random
import sys

from Crypto.Cipher import AES

sys.path.append("../set_1")
import challenge5


def decrypt_aes_128_cbc(key, iv, encbuf):
    block_size = 16

    if len(key) != 16: 
        print "key must be 16 bytes long"
        return

    if len(iv) != block_size:
        print "iv must be %d bytes long" % block_size
        return

    plainbuf = []
    last_enc_block = iv
    for i in range(0, len(encbuf), block_size):
        enc_block = encbuf[i:i+block_size]
    
        if len(enc_block) != block_size:
            print "enc_block requires %d bytes of padding" % (block_size - len(enc_block))
            return

        aes = AES.new(key)
        round1 = aes.decrypt(enc_block)

        plain_block = challenge5.repeating_xor(round1, last_enc_block)
        plainbuf.append(plain_block)

        last_enc_block = enc_block

    plainbuf = "".join(plainbuf)

    return plainbuf


def encrypt_aes_128_cbc(key, iv, plainbuf):
    block_size = 16

    if len(key) != 16: 
        print "key must be 16 bytes long"
        return

    if len(iv) != block_size:
        print "iv must be %d bytes long" % block_size
        return

    encbuf = []
    last_enc_block = iv
    for i in range(0, len(plainbuf), block_size):
        plain_block = plainbuf[i:i+block_size]
            
        if len(plain_block) != block_size:
            print "plain_block requires %d bytes of padding" % (block_size - len(plain_block))
            return

        round1 = challenge5.repeating_xor(plain_block, last_enc_block)

        aes = AES.new(key)
        enc_block = aes.encrypt(round1)
        encbuf.append(enc_block)

        last_enc_block = enc_block

    encbuf = "".join(encbuf)

    return encbuf


if __name__ == "__main__":
    # some tests
    key = "".join([chr(random.getrandbits(8)) for i in range(16)])
    iv = "".join([chr(random.getrandbits(8)) for i in range(16)])
    data = "".join([chr(random.getrandbits(8)) for i in range(32)])

    encbuf1 = encrypt_aes_128_cbc(key, iv, data)
    aes = AES.new(key, AES.MODE_CBC, iv)
    encbuf2 = aes.encrypt(data)
    if encbuf1 != encbuf2:
        print "bad test encryption"
        sys.exit(1)

    plainbuf1 = decrypt_aes_128_cbc(key, iv, encbuf1)
    aes = AES.new(key, AES.MODE_CBC, iv)
    plainbuf2 = aes.decrypt(encbuf1)
    if plainbuf1 != plainbuf2 != data:
        print "bad test decryption"
        sys.exit(1)

    fp = open("10.txt", "rb")
    data = fp.read()
    fp.close()

    data = data.strip()
    round1 = base64.b64decode(data)

    key = "YELLOW SUBMARINE"
    # aes blocksize is 16 bytes
    iv = "\x00"*16

    plaintext = decrypt_aes_128_cbc(key, iv, round1)
    if plaintext:
        print plaintext
