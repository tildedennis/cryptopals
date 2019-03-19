def xor_equal_len_hex_str(hex_str1, hex_str2):
    if len(hex_str1) != len(hex_str2):
        print "hex str lengths aren't equal"
        return

    hex_decoded1 = hex_str1.decode("hex")
    hex_decoded2 = hex_str2.decode("hex")

    out_raw = "".join([chr(ord(hex_decoded1[i]) ^ ord(hex_decoded2[i])) for i in range(len(hex_decoded1))])
    out = out_raw.encode("hex")

    return out


if __name__ == "__main__":
    out = xor_equal_len_hex_str("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965")
    if out == "746865206b696420646f6e277420706c6179":
        print out
