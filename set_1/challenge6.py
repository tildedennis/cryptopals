import base64
import sys

import challenge3
import challenge5


def str2bin(str1):
    str1_bin = []
    for c in str1:
        # [2:] to strip "0b"
        c_bin = bin(ord(c))[2:]
        # make sure all of them are 8-bits
        c_bin = "0"*(8-len(c_bin)) + c_bin
        str1_bin.append(c_bin)

    str1_bin = "".join(str1_bin)

    return str1_bin


def hamming_distance(str1, str2):
    str1_bin = str2bin(str1)
    str2_bin = str2bin(str2)

    if len(str1_bin) != len(str2_bin):
        print "str_bins aren't the same length"
        return

    diff_indexes = [i for i in range(len(str1_bin)) if str1_bin[i] != str2_bin[i]]
    distance = len(diff_indexes)

    return distance


def get_probable_key_size(data):
    distances = []
    for key_size in range(2, 41):
        chunk1 = data[0:key_size]
        chunk2 = data[key_size:(2*key_size)]
        chunk3 = data[(2*key_size):(3*key_size)]
        chunk4 = data[(3*key_size):(4*key_size)]

        distance1 = hamming_distance(chunk1, chunk2)
        distance2 = hamming_distance(chunk1, chunk3)
        distance3 = hamming_distance(chunk1, chunk4)
        distance4 = hamming_distance(chunk2, chunk3)
        distance5 = hamming_distance(chunk2, chunk4)
        distance6 = hamming_distance(chunk3, chunk4)

        avg_distance = (distance1+distance2+distance3+distance4+distance5+distance6)/6.0
        avg_distance_normalized = avg_distance/key_size

        distances.append((avg_distance_normalized, key_size))

    distances_sorted = sorted(distances, key=lambda x: x[0])

    probable_key_size = distances_sorted[0][1]
    print "probable key size: %d" % probable_key_size

    return probable_key_size


def get_probable_key(data):
    key_size = get_probable_key_size(data)

    blocks = []
    for offset in range(0, len(data), key_size):
        block = data[offset:offset+key_size]

        if len(block) != key_size:
            continue

        blocks.append(block)

    transposed_blocks = []
    for pos in range(key_size):
        transposed_block = []

        for block in blocks:
            transposed_block.append(block[pos])

        transposed_block = "".join(transposed_block)
        transposed_blocks.append(transposed_block)

    probable_key = []
    for transposed_block in transposed_blocks:
        high_score = 0
        single_byte_key = 0
        for test_key in range(0, 256):
            test_str = challenge3.single_byte_xor(transposed_block, test_key)
            score = challenge3.english_score(test_str)
            if score >= high_score:
                high_score = score
                single_byte_key = test_key

        probable_key.append(chr(single_byte_key))

    probable_key = "".join(probable_key)
    print "probable key: %s" % probable_key

    return probable_key


if __name__ == "__main__":
    # test hamming_distance
    if hamming_distance("this is a test", "wokka wokka!!!") != 37:
        print "bad hamming distance func"
        sys.exit(1)

    # break repeating xor key
    fp = open("6.txt", "rb")
    data = fp.read()
    fp.close()

    data = data.strip("\n")
    round1 = base64.b64decode(data)

    key = get_probable_key(round1)

    print
    print challenge5.repeating_xor(round1, key)
