import base64
import random
import sys

sys.path.append("../set_1")
import challenge7
import challenge9
import challenge11


def encryption_oracle(random_prefix, attacker_controlled, target_bytes, random_key):
    plainbuf = random_prefix + attacker_controlled + target_bytes
    padded_plainbuf = challenge9.pkcs7_pad(16, plainbuf)

    encbuf = challenge7.encrypt_aes_128_ecb(random_key, padded_plainbuf)

    return encbuf


if __name__ == "__main__":
    random_key = challenge11.get_rand_bytes(16)

    rand_size = random.randint(0, 64)
    random_prefix = challenge11.get_rand_bytes(rand_size)

    block_size = 16
    num_padded_bytes = block_size - 1
    base_block = chr(num_padded_bytes)*num_padded_bytes

    # dictionary of "<byte><0xf padding>" encbufs
    block_dict = {}
    for i in range(256):
        block = chr(i) + base_block
        encbuf = challenge7.encrypt_aes_128_ecb(random_key, block)
        block_dict[encbuf] = chr(i)

    unknown_string = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")

    plainbuf = []
    for b in unknown_string:
        # at some point within block_size, "<enc byte><0xf padding>" will be the last encrypted block
        for i in range(block_size):
            base_block = "A"*i
            encbuf = encryption_oracle(random_prefix, base_block, b, random_key)
            last_block = encbuf[-16:]
            try:
                if last_block in block_dict:
                    plain_byte = block_dict[last_block]
                    plainbuf.append(plain_byte)
                    break
            except KeyError:
                continue

    plainbuf = "".join(plainbuf)
    print plainbuf

    if plainbuf != unknown_string:
        print "bad decrypt"
        sys.exit(1)
