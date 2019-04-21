import random
import sys

sys.path.append("../set_1")
import challenge7
import challenge8
import challenge9
import challenge10


def get_rand_bytes(num):
    return "".join([chr(random.getrandbits(8)) for i in range(num)])


def encryption_oracle(plaintext):
    rand_key = get_rand_bytes(16)

    rand_size1 = random.randint(5, 10)
    rand_buf1 = get_rand_bytes(rand_size1)

    rand_size2 = random.randint(5, 10)
    rand_buf2 = get_rand_bytes(rand_size2)

    plainbuf = rand_buf1 + plaintext + rand_buf2
    plainbuf_padded = challenge9.pkcs7_pad(16, plainbuf)

    if random.randrange(2):
        mode = "ecb"
        encbuf = challenge7.encrypt_aes_128_ecb(rand_key, plainbuf_padded)
    else:
        mode = "cbc"
        rand_iv = get_rand_bytes(16)
        encbuf = challenge10.encrypt_aes_128_cbc(rand_key, rand_iv, plainbuf_padded)

    return encbuf, mode


if __name__ == "__main__":
    plaintext = "A"*(16*3)
    
    for i in range(1000000):
        encbuf, mode = encryption_oracle(plaintext)
        if challenge8.is_aes_ecb(encbuf):
            guessed_mode = "ecb"
        else:
            guessed_mode = "cbc"

        if guessed_mode != mode:
            print "bad mode guess (%d)" % i
