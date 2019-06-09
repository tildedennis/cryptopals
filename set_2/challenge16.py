import sys

sys.path.append("../set_1")
import challenge9
import challenge10
import challenge11
import challenge15


def generate_str(userdata):
    prepend = "comment1=cooking%20MCs;userdata="
    append = ";comment2=%20like%20a%20pound%20of%20bacon"

    # quote out ; and =
    userdata = userdata.replace(";", "").replace("=", "")

    combined = prepend + userdata + append

    return combined


def func1(rand_key, rand_iv, userdata):
    plainbuf = generate_str(userdata)
    plainbuf_padded = challenge9.pkcs7_pad(16, plainbuf)

    encbuf = challenge10.encrypt_aes_128_cbc(rand_key, rand_iv, plainbuf_padded)

    return encbuf


def func2(rand_key, rand_iv, encbuf):
    plainbuf_padded = challenge10.decrypt_aes_128_cbc(rand_key, rand_iv, encbuf)
    plainbuf = challenge15.pkcs7_unpad(plainbuf_padded)

    if ";admin=true;" in plainbuf:
        return plainbuf

    return


def split_into_blocks(encbuf):
    blocks = []
    for i in range(0, len(encbuf), 16):
        block = encbuf[i:i+16]
        blocks.append(block)

    return blocks


def bit_flip(byte, pos):
    # pos, 0 = lsb
    mask = 1 << pos 
    modded_byte = (byte ^ mask) & 0xff

    return modded_byte


def modify_block(block, byte_pos, bit_pos):
    # bit_pos, 0 = lsb
    # byte_pos, 0 = block[0]
    new_byte = bit_flip(ord(block[byte_pos]), bit_pos)
    new_block = block[:byte_pos] + chr(new_byte) + block[byte_pos+1:]

    return new_block


def modify_encbuf(encbuf, block_num, byte_pos, bit_pos):
    # bit_pos, 0 = lsb
    # byte_pos, 0 = block[0]
    # block_num, 0 = blocks[0]
    encbuf_blocks = split_into_blocks(encbuf)
    new_block = modify_block(encbuf_blocks[block_num], byte_pos, bit_pos)

    new_blocks = encbuf_blocks[:block_num] + [new_block] + encbuf_blocks[block_num+1:]
    new_encbuf = "".join(new_blocks)

    return new_encbuf


if __name__ == "__main__":
    rand_key = challenge11.get_rand_bytes(16)
    rand_iv = challenge11.get_rand_bytes(16)

    userdata = ":"*16 + ":admin<true"
    encbuf = func1(rand_key, rand_iv, userdata)

    # flip some bits
    # : -> ;
    #print bin(ord(split_into_blocks(encbuf)[2][0]))
    new_encbuf = modify_encbuf(encbuf, 2, 0, 0)
    #print bin(ord(split_into_blocks(new_encbuf)[2][0]))

    # < -> =
    #print bin(ord(split_into_blocks(encbuf)[2][6]))
    new_encbuf = modify_encbuf(new_encbuf, 2, 6, 0)
    #print bin(ord(split_into_blocks(new_encbuf)[2][6]))
    
    plainbuf = func2(rand_key, rand_iv, new_encbuf)
    if plainbuf:
        print "bitflips worked !"
        print plainbuf
