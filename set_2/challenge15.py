def pkcs7_unpad(padded_buf):
    possible_pad_byte = padded_buf[-1]
    pad_bytes = possible_pad_byte*ord(possible_pad_byte)
    if padded_buf[-ord(possible_pad_byte):] != pad_bytes:
        raise Exception("bad pad bytes")

    return padded_buf[:-ord(possible_pad_byte)]


if __name__ == "__main__":
    padded_buf1 = "ICE ICE BABY\x04\x04\x04\x04"
    try:
        buf1 = pkcs7_unpad(padded_buf1)
    except Exception as e:
        buf1 = None
        print e
        
    if buf1 != "ICE ICE BABY":
        print "bad unpadding1"

    padded_buf2 = "ICE ICE BABY\x05\x05\x05\x05"
    try:
        buf2 = pkcs7_unpad(padded_buf2)
    except Exception as e:
        buf2 = None
        print e
    if buf2 != "ICE ICE BABY":
        print "bad unpadding2"

    padded_buf3 = "ICE ICE BABY\x01\x02\x03\x04"
    try:
        buf3 = pkcs7_unpad(padded_buf3)
    except Exception as e:
        buf3 = None
        print e
    if buf3 != "ICE ICE BABY":
        print "bad unpadding3"
