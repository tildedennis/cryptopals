import collections
import sys

sys.path.append("../set_1")
import challenge7
import challenge9
import challenge11


def kv_parse(buf):
    obj = collections.OrderedDict()

    pieces = buf.split("&")
    for piece in pieces:
        key, value = piece.split("=")
        obj[key] = value

    return obj


def generate_obj(email):
    obj = collections.OrderedDict()

    obj["email"] = email
    obj["uid"] = 10
    obj["role"] = "user"

    return obj


def encode_obj(obj):
    pieces = []
    for key, value in obj.iteritems():
        pieces.append("%s=%s" % (key, value))

    encoded_obj = "&".join(pieces)

    return encoded_obj


def profile_for(email):
    # strip & and =
    email = email.replace("&", "").replace("=", "")

    obj = generate_obj(email)
    profile = encode_obj(obj)

    return profile


def encrypt_profile(key, profile):
    padded_profile = challenge9.pkcs7_pad(16, profile)
    enc_profile = challenge7.encrypt_aes_128_ecb(key, padded_profile)

    return enc_profile


def decrypt_profile(key, enc_profile):
    plain_profile = challenge7.decrypt_aes_128_ecb(key, enc_profile)
    unpadded_profile = challenge9.pkcs7_unpad(16, plain_profile)

    return unpadded_profile


if __name__ == "__main__":
    random_key = challenge11.get_rand_bytes(16)

    enc_blocks = []

    input1 = "A"*13
    enc_profile1 = encrypt_profile(random_key, profile_for(input1))
    # first 2 encrypted blocks decrypt to:
    # email=AAAAAAAAAAAAA&uid=10&role=
    enc_blocks.append(enc_profile1[:32])

    input2 = "A"*(16 - len("email=")) + challenge9.pkcs7_pad(16, "admin")
    enc_profile2 = encrypt_profile(random_key, profile_for(input2))
    # second encrypted block decrypts to:
    # admin\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b
    enc_blocks.append(enc_profile2[16:32])

    new_enc_profile = "".join(enc_blocks)
    plain_profile = decrypt_profile(random_key, new_enc_profile)
    print plain_profile

    profile_obj = kv_parse(plain_profile)
    print profile_obj
