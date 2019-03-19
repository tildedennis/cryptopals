import base64


def hex2base64(hex_str):
    hex_decoded = hex_str.decode("hex")
    #print "hex decoded: %s" % hex_decoded

    b64_encoded = base64.b64encode(hex_decoded)

    return b64_encoded


if __name__ == "__main__":
    out = hex2base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
    if out == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t":
        print out
