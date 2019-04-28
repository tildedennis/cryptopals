import base64
import sys

sys.path.append("../set_1")
import challenge7
import challenge11


def encryption_oracle(your_string, unknown_string, random_key):
    plainbuf = your_string + unknown_string
    encbuf = challenge7.encrypt_aes_128_ecb(random_key, plainbuf)

    return encbuf


def find_block_size(random_key):
    for i in range(128):
        plainbuf = "A"*i
        encbuf = encryption_oracle(plainbuf, "", random_key)
        if encbuf:
            return i


if __name__ == "__main__":
    random_key = challenge11.get_rand_bytes(16)

    block_size = find_block_size(random_key)
    print "block size is %d" % block_size

    base_block = "A"*(block_size-1)

    block_dict = {}
    for i in range(256):
        encbuf = encryption_oracle(base_block, chr(i), random_key)
        block_dict[encbuf] = chr(i)

    unknown_string = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

    plainbuf = []
    for b in unknown_string:
        encbuf = encryption_oracle(base_block, b, random_key)
        plain_byte = block_dict[encbuf]
        plainbuf.append(plain_byte)

    plainbuf = "".join(plainbuf)
    print plainbuf

    if plainbuf != unknown_string:
        print "bad decrypt"
        sys.exit(1)
