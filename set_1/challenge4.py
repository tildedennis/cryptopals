import challenge3


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
            test_str = challenge3.single_byte_xor(test_line, test_key)
            score = challenge3.english_score(test_str)
            if score >= high_score:
                high_score = score
                key = test_key
                line = test_line

    print "high score: %d" % high_score
    print "key: 0x%x" % key
    print line
    print challenge3.single_byte_xor(line, key)
