import collections


def single_byte_xor(buf, key):
    return "".join([chr(ord(c) ^ key) for c in buf])


def english_score(test_str):
    most_common_english_letters = "etaoinshrdlu"

    chr_counts = collections.Counter(test_str).most_common()
    score = 0
    for chr_count in chr_counts:
        index = most_common_english_letters.find(chr_count[0])
        if index != -1:
            # give more weight to more common letters
            score += (len(most_common_english_letters) - index) * chr_count[1]

    return score


if __name__ == "__main__":
    fp = open("4.txt", "rb")
    lines = fp.readlines()
    fp.close()

    high_score = 0
    key = 0
    line = None
    for test_line in lines:
        test_line = test_line.strip().decode("hex")

        for test_key in range(0, 0xff):
            test_str = single_byte_xor(test_line, test_key)
            score = english_score(test_str)
            if score >= high_score:
                high_score = score
                key = test_key
                line = test_line

    print "high score: %d" % high_score
    print "key: 0x%x" % key
    print line
    print single_byte_xor(line, key)
