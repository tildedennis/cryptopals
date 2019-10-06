import base64
import struct
import sys

sys.path.append("../set_1")
import challenge7


class AES128CTR:


    def __init__(self, key, nonce, counter):
        self.block_size = 16
        self.key = key
        self.nonce = nonce
        self.counter = counter


    def crypt(self, inbuf):
        outbuf = []
        for i, ib in enumerate(inbuf):
            if i % self.block_size == 0:
                ctr_data = struct.pack("QQ", self.nonce, self.counter)
                self.counter += 1
                keystream = challenge7.encrypt_aes_128_ecb(self.key, ctr_data)

            ob = ord(ib) ^ ord(keystream[i % len(keystream)])
            outbuf.append(chr(ob))

        return "".join(outbuf)


if __name__ == "__main__":
    encbuf_b64 = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    encbuf = base64.b64decode(encbuf_b64)

    aes_128_ctr = AES128CTR(key="YELLOW SUBMARINE", nonce=0, counter=0)
    plainbuf = aes_128_ctr.crypt(encbuf)
    print plainbuf

    aes_128_ctr = AES128CTR(key="YELLOW SUBMARINE", nonce=0, counter=0)
    checkbuf =  aes_128_ctr.crypt(plainbuf)
    checkbuf_b64 = base64.b64encode(checkbuf)
    if checkbuf_b64 != encbuf_b64:
        print "bad encrypt"
