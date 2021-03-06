from kalyna.key_expansion import KeyExpand
from tools import string2bytes, bytes2string


class KALYNA_TYPE:
    KALYNA_128_128 = {
        "Nk": 2,
        "Nb": 2,
        "Nr": 10
    }

    KALYNA_128_256 = {
        "Nk": 4,
        "Nb": 2,
        "Nr": 14
    }

    KALYNA_256_256 = {
        "Nk": 4,
        "Nb": 4,
        "Nr": 14
    }

    KALYNA_256_512 = {
        "Nk": 8,
        "Nb": 4,
        "Nr": 18
    }

    KALYNA_512_512 = {
        "Nk": 8,
        "Nb": 8,
        "Nr": 18
    }


class Kalyna:

    def __init__(self, key, kalyna_type=KALYNA_TYPE.KALYNA_128_128):

        self._key = key

        self._nk = kalyna_type["Nk"]
        self._nb = kalyna_type["Nb"]
        self._nr = kalyna_type["Nr"]

        self._words = KeyExpand(self._nb, self._nk, self._nr).expansion(key)

    @staticmethod
    def _add_round_key(state, key):
        for word, key_word in zip(state, key):
            for j in range(4):
                word[j] ^= key_word[j]

    def encrypt(self, plaintext):
        state = plaintext.copy()

        KeyExpand.add_round_key_expand(state, self._words[0])
        for word in self._words[1:-1]:
            state = KeyExpand.encipher_round(state, self._nb)
            KeyExpand.xor_round_key_expand(state, word)

        state = KeyExpand.encipher_round(state, self._nb)
        KeyExpand.add_round_key_expand(state, self._words[-1])

        return state

    def decrypt(self, ciphertext):
        state = ciphertext.copy()

        KeyExpand.sub_round_key_expand(state, self._words[-1])
        for word in self._words[1:-1][::-1]:
            state = KeyExpand.decipher_round(state, self._nb)
            KeyExpand.xor_round_key_expand(state, word)

        state = KeyExpand.decipher_round(state, self._nb)
        KeyExpand.sub_round_key_expand(state, self._words[0])

        return state


if __name__ == '__main__':
    key_test = string2bytes("000102030405060708090A0B0C0D0E0F")
    plaintext = string2bytes("101112131415161718191A1B1C1D1E1F")

    kalyna_128_128 = Kalyna(key_test, KALYNA_TYPE.KALYNA_128_128)

    ciphertext = kalyna_128_128.encrypt(plaintext)
    print(bytes2string(ciphertext))
    re_plaintext = kalyna_128_128.decrypt(ciphertext)
    print(bytes2string(re_plaintext))
    print(re_plaintext == plaintext)

    print("\n****\n")

    key_test = string2bytes("000102030405060708090A0B0C0D0E0F"
                            "101112131415161718191A1B1C1D1E1F")

    kalyna_128_256 = Kalyna(key_test, KALYNA_TYPE.KALYNA_128_256)

    ciphertext = kalyna_128_256.encrypt(plaintext)
    print(bytes2string(ciphertext))
    re_plaintext = kalyna_128_256.decrypt(ciphertext)
    print(bytes2string(re_plaintext))
    print(re_plaintext == plaintext)

    print("\n****\n")

    key_test = string2bytes("000102030405060708090A0B0C0D0E0F"
                            "101112131415161718191A1B1C1D1E1F")

    kalyna_256_256 = Kalyna(key_test, KALYNA_TYPE.KALYNA_256_256)
    plaintext = string2bytes("202122232425262728292A2B2C2D2E2F"
                             "303132333435363738393A3B3C3D3E3F")

    ciphertext = kalyna_256_256.encrypt(plaintext)
    print(bytes2string(ciphertext))
    re_plaintext = kalyna_256_256.decrypt(ciphertext)
    print(bytes2string(re_plaintext))
    print(re_plaintext == plaintext)

    print("\n****\n")

    key_test = string2bytes("000102030405060708090A0B0C0D0E0F"
                            "101112131415161718191A1B1C1D1E1F"
                            "202122232425262728292A2B2C2D2E2F"
                            "303132333435363738393A3B3C3D3E3F")

    kalyna_256_512 = Kalyna(key_test, KALYNA_TYPE.KALYNA_256_512)
    plaintext = string2bytes("404142434445464748494A4B4C4D4E4F"
                             "505152535455565758595A5B5C5D5E5F")

    ciphertext = kalyna_256_512.encrypt(plaintext)
    print(bytes2string(ciphertext))
    re_plaintext = kalyna_256_512.decrypt(ciphertext)
    print(bytes2string(re_plaintext))
    print(re_plaintext == plaintext)

    print("\n****\n")

    key_test = string2bytes("000102030405060708090A0B0C0D0E0F"
                            "101112131415161718191A1B1C1D1E1F"
                            "202122232425262728292A2B2C2D2E2F"
                            "303132333435363738393A3B3C3D3E3F")

    kalyna_512_512 = Kalyna(key_test, KALYNA_TYPE.KALYNA_512_512)
    plaintext = string2bytes("404142434445464748494A4B4C4D4E4F"
                             "505152535455565758595A5B5C5D5E5F"
                             "606162636465666768696A6B6C6D6E6F"
                             "707172737475767778797A7B7C7D7E7F")

    ciphertext = kalyna_512_512.encrypt(plaintext)
    print(bytes2string(ciphertext))
    re_plaintext = kalyna_512_512.decrypt(ciphertext)
    print(bytes2string(re_plaintext))
    print(re_plaintext == plaintext)
