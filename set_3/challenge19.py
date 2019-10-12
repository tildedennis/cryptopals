import base64
import collections
import sys

sys.path.append("../set_1")
sys.path.append("../set_2")
import challenge5
import challenge11
import challenge18


def get_ciphertexts():
    plaintexts = [
        'SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==',
        'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=',
        'RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==',
        'RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=',
        'SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk',
        'T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
        'T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=',
        'UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==',
        'QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=',
        'T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl',
        'VG8gcGxlYXNlIGEgY29tcGFuaW9u',
        'QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==',
        'QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=',
        'QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==',
        'QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=',
        'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
        'VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==',
        'SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==',
        'SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==',
        'VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==',
        'V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==',
        'V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==',
        'U2hlIHJvZGUgdG8gaGFycmllcnM/',
        'VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=',
        'QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=',
        'VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=',
        'V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=',
        'SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==',
        'U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==',
        'U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=',
        'VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==',
        'QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu',
        'SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=',
        'VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs',
        'WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=',
        'SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0',
        'SW4gdGhlIGNhc3VhbCBjb21lZHk7',
        'SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=',
        'VHJhbnNmb3JtZWQgdXR0ZXJseTo=',
        'QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=',
    ]

    rand_key = challenge11.get_rand_bytes(16)

    ciphertexts = []
    check_plaintexts = []
    for plaintext in plaintexts:
        aes_128_ctr = challenge18.AES128CTR(key=rand_key, nonce=0, counter=0)
        ciphertext = aes_128_ctr.crypt(base64.b64decode(plaintext))
        ciphertexts.append(ciphertext)
        check_plaintexts.append(base64.b64decode(plaintext))

    return ciphertexts, check_plaintexts


def get_keystream_size(ciphertexts):
    keystream_size = 0
    for ciphertext in ciphertexts:
        if len(ciphertext) > keystream_size:
            keystream_size = len(ciphertext)

    return keystream_size


def print_plaintexts(ciphertexts, key_stream, marker=None):
    plaintexts = []
    for i, ciphertext in enumerate(ciphertexts):
        plaintext = challenge5.repeating_xor(ciphertext, key_stream)
        plaintexts.append(plaintext)

        if marker is not None:
            plaintext = plaintext[:marker] + "|||" + plaintext[marker:]

        print "%d: %s" % (i, repr(plaintext))

    return plaintexts


def get_gram_counts(ciphertexts, start, stop):
    grams = []

    for ciphertext in ciphertexts:
        gram = ciphertext[start:stop]
        grams.append(gram)

    gram_counts = collections.Counter(grams).most_common(5)

    return gram_counts


if __name__ == "__main__":
    ciphertexts, check_plaintexts = get_ciphertexts()

    keystream_size = get_keystream_size(ciphertexts)
    keystream = bytearray("\x00") * keystream_size

    for pos in range(keystream_size):
        print "working on pos %d/%d" % (pos, keystream_size)
        next_pos = False
        
        while not next_pos:
            plaintexts = print_plaintexts(ciphertexts, str(keystream), pos)

            if pos == 0:
                gram_counts = get_gram_counts(ciphertexts, 0, 3)
                print gram_counts

            line_number = raw_input("which line number? ")
            try:
                line_number = int(line_number)
            except:
                print "bad line number: %s" % line_number
                continue

            if line_number < 0 or line_number >= len(plaintexts):
                print "bad line number: %d" % line_number
                continue

            selected_ciphertext = ciphertexts[line_number]
            selected_plaintext = plaintexts[line_number]
            print "selected ciphertext: %s" % repr(selected_ciphertext)
            print "selected plaintext: %s" % repr(selected_plaintext)

            plaintext_guess = raw_input("plaintext guess for pos %d? " % pos)
            if len(plaintext_guess) != 1:
                print "bad guess: %s" % plaintext_guess
                continue

            old_keystream = keystream[:]
            keystream[pos] = ord(selected_ciphertext[pos]) ^ ord(plaintext_guess)
            print_plaintexts(ciphertexts, str(keystream), (pos+1))

            move_pos = raw_input("move to next pos? ")
            if move_pos.lower().startswith("y"):
                next_pos = True
            else:
                keystream = old_keystream
                next_pos = False
                
    plaintexts = print_plaintexts(ciphertexts, str(keystream))
    if plaintexts != check_plaintexts:
        print "bad decrypts"
