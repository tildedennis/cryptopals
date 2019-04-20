import base64
import sys

from Crypto.Cipher import AES


def decrypt_aes_128_ecb(key, encbuf):
    block_size = 16

    if len(key) != 16:
        print "key must be 16 bytes long"
        return

    plainbuf = []
    for i in range(0, len(encbuf), block_size):
        enc_block = encbuf[i:i+block_size]
        
        if len(enc_block) != block_size:
            print "enc_block requires %d bytes of padding" % (block_size - len(enc_block))
            return

        aes = AES.new(key)
        plain_block = aes.decrypt(enc_block)
        plainbuf.append(plain_block)

    plainbuf = "".join(plainbuf)

    return plainbuf


def encrypt_aes_128_ecb(key, plainbuf):
    block_size = 16

    if len(key) != 16:
        print "key must be 16 bytes long"
        return

    encbuf = []
    for i in range(0, len(plainbuf), block_size):
        plain_block = plainbuf[i:i+block_size]

        if len(plain_block) != block_size:
            print "plain_block requires %d bytes of padding" % (block_size - len(plain_block))
            return

        aes = AES.new(key)
        enc_block = aes.encrypt(plain_block)
        encbuf.append(enc_block)

    encbuf = "".join(encbuf)

    return encbuf


if __name__ == "__main__":
    fp = open("7.txt", "rb")
    data = fp.read()
    fp.close()

    data = data.strip("\n")
    round1 = base64.b64decode(data)

    key = "YELLOW SUBMARINE"
    plaintext = decrypt_aes_128_ecb(key, round1)
    if plaintext:
        print plaintext

    test_encbuf = encrypt_aes_128_ecb(key, plaintext)
    if test_encbuf != round1:
        print "bad test encrypt"
        sys.exit(1)
