from keygen import generate_decoder_key
from tokengen import bin_pad, bin_str, generate_token_block


def start_point(decoder_key, token_block):
    start_point_int = int(decoder_key, base=2) ^ int(token_block, base=2)
    start_point_bin_str = bin_pad(bin_str(start_point_int), 64)
    return start_point_bin_str


start_point = start_point(generate_decoder_key(), generate_token_block())


def nibbleate(bits64_string):
    nibbles = []
    for i in range(0, len(bits64_string), 4):
        nibbles.append(bits64_string[i: i + 4])
    return nibbles


def substitute(bits64_string):
    tables = {
        1: [4, 6, 0, 9, 2, 8, 7, 5, 14, 12, 3, 15, 13, 10, 11, 1],
        2: [2, 15, 4, 10, 0, 7, 1, 6, 5, 3, 13, 14, 9, 12, 8, 11]
    }

    nibbles = nibbleate(bits64_string)
    enumerated_nibbles = list(zip(list(range(len(nibbles))), nibbles))

    for i, nibble in enumerated_nibbles:
        if nibble[0] == '0':
            table = tables[1]
            nibbles[i] = table[i]
        else:
            table = tables[2]
            nibbles[i] = table[i]

    substituted_nibbles = list(map(lambda x: bin_pad(bin_str(x), 4), nibbles))

    return substituted_nibbles

def permutate(bits64_string):
    table = []
