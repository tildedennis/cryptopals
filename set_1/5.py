def repeating_xor(in_buf, key):
    out_buf = []

    for i, ib in enumerate(in_buf):
        ob = ord(ib) ^ ord(key[i % len(key)])
        out_buf.append(chr(ob))

    out_buf = "".join(out_buf)

    return out_buf


if __name__ == "__main__":
    in_buf = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"

    out_buf = repeating_xor(in_buf, "ICE")
    if out_buf.encode("hex") == "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f":
        print out_buf.encode("hex")
    else:
        print "incorrect xor"
