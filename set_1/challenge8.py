def is_aes_ecb(encbuf):
    block_size = 16

    if len(encbuf) % block_size != 0:
        print "not a multiple of block size %d" % block_size
        return

    blocks = []
    for i in range(0, len(encbuf), block_size):
        block = encbuf[i:i+block_size]
        blocks.append(block)

    dup_blocks = [b for b in blocks if blocks.count(b) > 1]

    return dup_blocks


if __name__ == "__main__":
    fp = open("8.txt", "rb")
    lines = fp.readlines()
    fp.close()

    for line in lines:
        line = line.strip()

        dup_blocks = is_aes_ecb(line.decode("hex"))
        if dup_blocks:
            print "%s (%d dup blocks)" % (line, len(dup_blocks))
