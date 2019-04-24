import copy

plain_text = [0b1101, 0b0111, 0b0010, 0b1000]
print('Plain text', plain_text)
key = [0b0100, 0b1010, 0b1111, 0b0101]
k0 = copy.deepcopy(key)
k1 = [0, 0, 0, 0]
k2 = [0, 0, 0, 0]
sbox1 = [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7]
sbox2 = [10, 5, 9, 11, 1, 7, 8, 15, 6, 0, 2, 3, 12, 4, 13, 14]

mul_table = {
    2: [0, 2, 4, 6, 8, 10, 12, 14, 3, 1, 7, 5, 11, 9, 15, 13],
    4: [0, 4, 8, 12, 3, 7, 11, 15, 6, 2, 14, 10, 5, 1, 13, 9],
    9: [0, 9, 1, 8, 2, 11, 3, 10, 4, 13, 5, 12, 6, 15, 7, 14],
    1: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
}


def g(sbox, cur_key, xor):
    # print('start', cur_key)
    swapped = [cur_key[1], cur_key[0]]
    # print(swapped)
    subs = [sbox[swapped[0]], sbox[swapped[1]]]
    # print(subs)
    ans = [subs[0] ^ xor[0], subs[1] ^ xor[1]]
    # print(ans)
    return ans


def xor(l1, l2):
    return [l1[i] ^ l2[i] for i in range(len(l1))]


def sbox_substitution(sbox, l1):
    return [sbox[i] for i in l1]


def key_generation():
    global k0, k1, k2
    cur_g = g(sbox1, [k0[2], k0[3]], [0b1000, 0b0000])

    k1[0], k1[1] = cur_g[0] ^ k0[0], cur_g[1] ^ k0[1]

    k1[2] = k1[0] ^ k0[2]
    k1[3] = k1[1] ^ k0[3]

    cur_g = g(sbox1, [k1[2], k1[3]], [0b0011, 0b0000])

    k2[0], k2[1] = cur_g[0] ^ k1[0], cur_g[1] ^ k1[1]

    k2[2] = k2[0] ^ k1[2]
    k2[3] = k2[1] ^ k1[3]


def mix_col(val, to_multiply, inverse=False):
    val_mat = val
    if inverse == False:
        val_mat = [[val[0], val[2]], [val[1], val[3]]]
    else:
        to_multiply = [[to_multiply[0], to_multiply[1]], [to_multiply[2], to_multiply[3]]]

    res_mat = [0, 0, 0, 0]
    counter = 0
    for i in val_mat:
        for j in to_multiply:
            # print(j[0], i[0], j[1], i[1])
            if inverse == False:
                res_mat[counter] = mul_table[j[0]][i[0]] ^ mul_table[j[1]][i[1]]
            else:
                res_mat[counter] = mul_table[i[0]][j[0]] ^ mul_table[i[1]][j[1]]
            counter += 1

        # print(res_mat)
    return res_mat


key_generation()


# print(k1)
# print(k2)


def e_round(text, cur_key, sbox, to_mix):
    round_text = xor(cur_key, text)

    subs = sbox_substitution(sbox1, round_text)

    subs[1], subs[3] = subs[3], subs[1]
    if to_mix:
        mix = mix_col(subs, [[1, 4], [4, 1]])

        return mix

    return subs


def d_round(text, cur_key, sbox, to_mix):
    text[1], text[3] = text[3], text[1]
    # print('shift', text)
    subs = sbox_substitution(sbox, text)
    # print('sbox', subs)
    round_text = xor(subs, cur_key)
    # print('xor', round_text)
    if to_mix:
        mix = mix_col([[9, 2], [2, 9]], round_text, True)
        # print('mix', mix)
        return mix

    return round_text


r0 = e_round(plain_text, k0, sbox1, True)
r1 = e_round(r0, k1, sbox1, False)
# print(r1)
r2 = xor(r1, k2)
print('cipher text', r2)

d0 = xor(r2, k2)
# print('xor', d0)
d1 = d_round(d0, k1, sbox2, True)
d2 = d_round(d1, k0, sbox2, False)
print('decrypted', d2)

'''
Plain text [13, 7, 2, 8]
cipher text [2, 4, 14, 12]
decrypted [13, 7, 2, 8]
'''