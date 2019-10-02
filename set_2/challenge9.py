import struct
import sys


def pkcs7_pad(block_size, buf):
    # if multiple of block size, add block size padding so that we know the last byte is padding
    if len(buf) % block_size == 0:
        pad_byte = struct.pack("B", block_size)
        padded_buf = buf + (pad_byte*block_size)
        return padded_buf

    complete_blocks = len(buf) / block_size
    padded_size = (complete_blocks + 1) * block_size
    num_padding_bytes = padded_size - len(buf)
    pad_byte = struct.pack("B", num_padding_bytes)

    padded_buf = buf + (pad_byte*num_padding_bytes)
    if len(padded_buf) % block_size != 0:
        print "bad padding added"
        return buf

    return padded_buf


def pkcs7_unpad(block_size, padded_buf):
    if len(padded_buf) % block_size != 0:
        print "bad padded length"
        return padded_buf

    possible_pad_byte = padded_buf[-1]
    pad_bytes = possible_pad_byte*ord(possible_pad_byte)
    if padded_buf[-ord(possible_pad_byte):] != pad_bytes:
        return padded_buf

    return padded_buf[:-ord(possible_pad_byte)]


if __name__ == "__main__":
    block_size = 20

    print "padding"
    buf1 = "A"*block_size
    padded_buf1 = pkcs7_pad(block_size, buf1)
    print "%s (%d bytes)" % (padded_buf1, len(padded_buf1))

    buf2 = "YELLOW SUBMARINE"
    padded_buf2 = pkcs7_pad(block_size, "YELLOW SUBMARINE")
    print "%s (%d bytes)" % (padded_buf2, len(padded_buf2))
    if padded_buf2 != "YELLOW SUBMARINE\x04\x04\x04\x04":
        print "bad padding"
        sys.exit(1)

    print "unpadding"
    unpadded_buf1 = pkcs7_unpad(block_size, padded_buf1)
    print "%s (%d bytes)" % (unpadded_buf1, len(unpadded_buf1))
    if unpadded_buf1 != buf1:
        print "bad unpadding"
        sys.exit(1)

    unpadded_buf2 = pkcs7_unpad(block_size, padded_buf2)
    print "%s (%d bytes)" % (unpadded_buf2, len(unpadded_buf2))
    if unpadded_buf2 != buf2:
        print "bad unpadding"
        sys.exit(1)

    buf3 = "A"*34
    padded_buf3 = pkcs7_pad(16, buf3)
    if padded_buf3 != "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e":
        print "bad padding"
        sys.exit(1)

    unpadded_buf3 = pkcs7_unpad(16, padded_buf3)
    if unpadded_buf3 != buf3:
        print "bad unpadding"
        sys.exit(1)
