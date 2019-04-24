S_BOX = [[9, 4, 10, 11], [13, 1, 8, 5], [6, 2, 0, 3], [12, 14, 15, 7]]
S_BOX_INV = [[10, 5, 9, 11], [1, 7, 8, 15], [6, 0, 2, 3], [12, 4, 13, 14]]
MUL_TABLE = {
    2: [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
    4: [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
    9: [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
    1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
}
KEY = '0100101011110101'
K0 = ''
K1 = ''
K2 = ''


def left_bits(text):
    return text[:int(len(text) / 2)]


def right_bits(text):
    return text[int(len(text) / 2):]


def xor(n1, n2):
    new = ''
    for a, b in zip(n1, n2):
        new += str(int(a) ^ int(b))
    return new


def s_box_substitution(text, s_box):
    # row = int(text[0] + text[3], 2)
    # col = int(text[1] + text[2], 2)
    return "{0:04b}".format(s_box[int(left_bits(text), 2)][int(right_bits(text), 2)])


def g_func(key, xor_key):
    L = left_bits(key)
    R = right_bits(key)
    new = R + L
    new = s_box_substitution(left_bits(new), S_BOX) + s_box_substitution(right_bits(new), S_BOX)
    return xor(new, xor_key)


def generate_keys():
    global K0, K1, K2

    w0 = left_bits(KEY)
    w1 = right_bits(KEY)
    K0 = w0 + w1

    temp = g_func(w1, '10000000')
    w2 = xor(temp, w0)
    w3 = xor(w2, w1)
    K1 = w2 + w3

    temp = g_func(w3, '00110000')
    w4 = xor(temp, w2)
    w5 = xor(w4, w3)
    K2 = w4 + w5


def mix_cols(text, mat, inverse=False):
    s0 = text[0:4]
    s1 = text[4:8]
    s2 = text[8:12]
    s3 = text[12:16]

    if not inverse:
        m0 = xor('{0:04b}'.format(MUL_TABLE[mat[0]][int(s0, 2)]), '{0:04b}'.format(MUL_TABLE[mat[2]][int(s2, 2)]))
        m1 = xor('{0:04b}'.format(MUL_TABLE[mat[0]][int(s1, 2)]), '{0:04b}'.format(MUL_TABLE[mat[2]][int(s3, 2)]))
        m2 = xor('{0:04b}'.format(MUL_TABLE[mat[1]][int(s0, 2)]), '{0:04b}'.format(MUL_TABLE[mat[3]][int(s2, 2)]))
        m3 = xor('{0:04b}'.format(MUL_TABLE[mat[1]][int(s1, 2)]), '{0:04b}'.format(MUL_TABLE[mat[3]][int(s3, 2)]))

        return m0 + m2 + m1 + m3

    else:
        m0 = xor('{0:04b}'.format(MUL_TABLE[mat[0]][int(s0, 2)]), '{0:04b}'.format(MUL_TABLE[mat[2]][int(s1, 2)]))
        m1 = xor('{0:04b}'.format(MUL_TABLE[mat[1]][int(s0, 2)]), '{0:04b}'.format(MUL_TABLE[mat[3]][int(s1, 2)]))
        m2 = xor('{0:04b}'.format(MUL_TABLE[mat[0]][int(s2, 2)]), '{0:04b}'.format(MUL_TABLE[mat[2]][int(s3, 2)]))
        m3 = xor('{0:04b}'.format(MUL_TABLE[mat[1]][int(s2, 2)]), '{0:04b}'.format(MUL_TABLE[mat[3]][int(s3, 2)]))

        return m0 + m1 + m2 + m3


def encrypt(text):
    # Round 0
    temp = xor(text, K0)

    # Round 1
    nibble_sub = ''
    for i in range(0, len(temp), 4):
        nibble_sub += s_box_substitution(temp[i:i + 4], S_BOX)
    shift_row = nibble_sub[0:4] + nibble_sub[12:16] + nibble_sub[8:12] + nibble_sub[4:8]
    mixed_cols = mix_cols(shift_row, [1, 4, 4, 1])
    temp = xor(mixed_cols, K1)

    # Round 2
    nibble_sub = ''
    for i in range(0, len(temp), 4):
        nibble_sub += s_box_substitution(temp[i:i + 4], S_BOX)
    shift_row = nibble_sub[0:4] + nibble_sub[12:16] + nibble_sub[8:12] + nibble_sub[4:8]

    return xor(shift_row, K2)


def decrypt(cipher):
    # Round 0
    temp = xor(cipher, K2)

    # Round 1
    shift_row = temp[0:4] + temp[12:16] + temp[8:12] + temp[4:8]
    nibble_sub = ''
    for i in range(0, len(temp), 4):
        nibble_sub += s_box_substitution(shift_row[i:i + 4], S_BOX_INV)
    temp = xor(nibble_sub, K1)
    mixed_cols = mix_cols(temp, [9, 2, 2, 9],True)

    # Round 2
    shift_row = mixed_cols[0:4] + mixed_cols[12:16] + mixed_cols[8:12] + mixed_cols[4:8]
    nibble_sub = ''
    for i in range(0, len(temp), 4):
        nibble_sub += s_box_substitution(shift_row[i:i + 4], S_BOX_INV)
    temp = xor(nibble_sub, K0)

    return temp


def main():
    plain_text = '1101011100101000'
    generate_keys()
    cipher = encrypt(plain_text)
    print(plain_text)
    print(cipher)
    print(decrypt(cipher))


main()
