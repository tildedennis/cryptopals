import base64
import sys 

sys.path.append("../set_1")
sys.path.append("../set_2")
import challenge5
import challenge6
import challenge11
import challenge18


def get_ciphertexts(plaintexts):
    rand_key = challenge11.get_rand_bytes(16)

    ciphertexts = []
    for plaintext in plaintexts:
        aes_128_ctr = challenge18.AES128CTR(key=rand_key, nonce=0, counter=0)
        ciphertext = aes_128_ctr.crypt(base64.b64decode(plaintext))
        ciphertexts.append(ciphertext)

    return ciphertexts


if __name__ == "__main__":
    fp = open("20.txt", "rb")
    lines = fp.readlines()
    fp.close()
    lines = [l.strip() for l in lines]

    ciphertexts = get_ciphertexts(lines)

    smallest_len = min([len(c) for c in ciphertexts])
    truncated_ciphertexts = [c[:smallest_len] for c in ciphertexts]
    concatenated_ciphertexts = "".join(truncated_ciphertexts)

    key = challenge6.get_probable_key(concatenated_ciphertexts, smallest_len, smallest_len+1)
    concatenated_plaintexts = challenge5.repeating_xor(concatenated_ciphertexts, key)
    print concatenated_plaintexts
