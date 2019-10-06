import base64
import random
import sys

sys.path.append("../set_2")
import challenge9
import challenge10
import challenge11
import challenge15
import challenge16


def func1(key):
    strings = [
        "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
    ]

    choice = base64.b64decode(random.choice(strings))
    choice_padded = challenge9.pkcs7_pad(16, choice)

    iv = challenge11.get_rand_bytes(16)

    ciphertext = challenge10.encrypt_aes_128_cbc(key, iv, choice_padded)

    return choice, ciphertext, iv


def func2(key, iv, ciphertext):
    plaintext_padded = challenge10.decrypt_aes_128_cbc(key, iv, ciphertext)

    try:
        plaintext = challenge15.pkcs7_unpad(plaintext_padded)
        return True
    except Exception as err:
        pass

    return False


if __name__ == "__main__":
    rand_key = challenge11.get_rand_bytes(16)
    # choice only used to verify decrypt
    choice, ciphertext, iv = func1(rand_key)

    block_size = 16

    blocks = []
    blocks.append(iv)
    blocks += challenge16.split_into_blocks(ciphertext)

    plainblocks = []
    for block_num in range(0, len(blocks)-1):
        plainblock = bytearray("\x00") * block_size
        block1 = bytearray(blocks[block_num])
        original_block1 = block1
        block2 = blocks[block_num+1]

        for pos in range(15, -1, -1):
            padding_byte = block_size - pos
            for mod_byte in range(256):
                modded_block1 = bytearray(block1)
                modded_block1[pos] = mod_byte

                if func2(rand_key, str(modded_block1), block2):
                    plain_chr = original_block1[pos] ^ mod_byte ^ padding_byte

                    # last block special case
                    # actual padding can be found first
                    if padding_byte == 1 and plain_chr == padding_byte:
                        continue

                    plainblock[pos] = chr(plain_chr)

                    next_padding_byte = padding_byte + 1
                    for i in range(pos, block_size):
                        modded_block1[i] = original_block1[i] ^ plainblock[i] ^ next_padding_byte

                    block1 = modded_block1
                    break

        plainblocks += plainblock

plainbuf = challenge15.pkcs7_unpad("".join([chr(b) for b in plainblocks]))
print plainbuf
print choice

if plainbuf != choice:
    print "bad decrypt"
