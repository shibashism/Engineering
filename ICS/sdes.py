IP = [2, 6, 3, 1, 4, 8, 5, 7]
inverse_IP = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]
S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

KEY = '0111111101'


def permute(text, key):
    new_text = ''
    for i in key:
        new_text += (text[i - 1])
    return new_text


def left_bits(text):
    return text[:int(len(text) / 2)]


def right_bits(text):
    return text[int(len(text) / 2):]


def shift(text, bits):
    return text[bits:] + text[:-(len(text) - bits)]


def xor(n1, n2):
    new = ''
    for a, b in zip(n1, n2):
        new += str(int(a) ^ int(b))
    return new


def key_1():
    temp = permute(KEY, P10)
    left = shift(left_bits(temp), 1)
    right = shift(right_bits(temp), 1)
    temp = left + right
    return permute(temp, P8)


def key_2():
    temp = permute(KEY, P10)
    left = shift(left_bits(temp), 3)
    right = shift(right_bits(temp), 3)
    temp = left + right
    return permute(temp, P8)


def s_box_substitution(text, s_box):
    row = int(text[0] + text[3], 2)
    col = int(text[1] + text[2], 2)
    return "{0:02b}".format(s_box[row][col])


def f_k(text, key):
    left = left_bits(text)
    right = right_bits(text)
    new_right = permute(right, EP)
    new_right = xor(new_right, key)
    temp = s_box_substitution(left_bits(new_right), S0) + s_box_substitution(right_bits(new_right), S1)
    temp = permute(temp, P4)
    return xor(left, temp) + right


def switch(text):
    return right_bits(text) + left_bits(text)


def encrypt(plain_text):
    initial = permute(plain_text, IP)
    first_key = f_k(initial, key_1())
    switched = switch(first_key)
    second_key = f_k(switched, key_2())
    final = permute(second_key, inverse_IP)
    return final


def decrypt(cipher):
    initial = permute(cipher, IP)
    second_key = f_k(initial, key_2())
    switched = switch(second_key)
    first_key = f_k(switched, key_1())
    final = permute(first_key, inverse_IP)
    return final


def main():
    plain_text = '11101010'
    cipher = encrypt(plain_text)
    print(cipher)
    print(decrypt(cipher))


main()
