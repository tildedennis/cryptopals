import base64
import sys

from Crypto.Cipher import AES


def aes_128_ebc(key, encbuf):
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


if __name__ == "__main__":
    fp = open("7.txt", "rb")
    data = fp.read()
    fp.close()

    data = data.strip("\n")
    round1 = base64.b64decode(data)

    key = "YELLOW SUBMARINE"
    plaintext = aes_128_ebc(key, round1)
    if plaintext:
        print plaintext
