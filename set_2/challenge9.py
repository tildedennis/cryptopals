import struct
import sys


def pkcs7_pad(block_size, block):
    if len(block) % block_size == 0:
        return block

    complete_blocks = len(block) / block_size
    padded_size = (complete_blocks + 1) * block_size
    num_padding_bytes = padded_size - len(block)
    pad_byte = struct.pack("B", num_padding_bytes)

    padded_block = block + (pad_byte*num_padding_bytes)
    if len(padded_block) % block_size != 0:
        print "bad padding added"
        return block

    return padded_block


def pkcs7_unpad(block_size, padded_block):
    if len(padded_block) != block_size:
        print "bad padded length"
        return padded_block

    possible_pad_byte = padded_block[-1]
    if ord(possible_pad_byte) >= len(padded_block):
        return padded_block

    pad_bytes = possible_pad_byte*ord(possible_pad_byte)
    if padded_block[-ord(possible_pad_byte):] != pad_bytes:
        return padded_block

    return padded_block[:-ord(possible_pad_byte)]


if __name__ == "__main__":
    block_size = 20

    print "padding"
    block1 = "A"*block_size
    padded_block1 = pkcs7_pad(block_size, block1)
    print "%s (%d bytes)" % (padded_block1, len(padded_block1))

    block2 = "YELLOW SUBMARINE"
    padded_block2 = pkcs7_pad(block_size, "YELLOW SUBMARINE")
    print "%s (%d bytes)" % (padded_block2, len(padded_block2))
    if padded_block2 != "YELLOW SUBMARINE\x04\x04\x04\x04":
        print "bad padding"
        sys.exit(1)

    print "unpadding"
    unpadded_block1 = pkcs7_unpad(block_size, padded_block1)
    print "%s (%d bytes)" % (unpadded_block1, len(unpadded_block1))
    if unpadded_block1 != block1:
        print "bad unpadding"
        sys.exit(1)

    unpadded_block2 = pkcs7_unpad(block_size, padded_block2)
    print "%s (%d bytes)" % (unpadded_block2, len(unpadded_block2))
    if unpadded_block2 != block2:
        print "bad unpadding"
        sys.exit(1)

    block = "A"*34
    padded_block = pkcs7_pad(16, block)
    if padded_block != "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e":
        print "bad padding"
        sys.exit(1)
