from datetime import timedelta
from functools import reduce
from Crypto.Cipher import DES

from keygen import generate_decoder_key
from tokencipher_sts import class_insert, token_nibbleate
from tokengen import bin_pad, bin_str, concat_str, crc16, generate_token_block, base_date, token_class, rate


def post_encryption(encrypted):
    bits64_encrypted = bin_pad(bin_str(int(encrypted.hex(), base=16)), 64)
    class_inserted_encrypted = class_insert(bits64_encrypted)
    nibblated, unnibblated = token_nibbleate(class_inserted_encrypted)
    return nibblated, unnibblated


# token_block = generate_token_block()
# decoder_key = generate_decoder_key()
iv = b'\x17\xb2\x86\xed1\x9a\x15\xf2'


def encrypt(token_block, decoder_key):
    token_block_int = int(token_block, base=2)
    decoder_key_int = int(decoder_key, base=2)

    token_block_hex_padded = bin_pad(hex(token_block_int).lstrip('0x'), 16)
    decoder_key_hex_padded = bin_pad(hex(decoder_key_int).lstrip('0x'), 16)

    byte_arrayed_token_block = bytearray.fromhex(token_block_hex_padded)
    byte_arrayed_decoder_key = bytearray.fromhex(decoder_key_hex_padded)

    cipher = DES.new(byte_arrayed_decoder_key, DES.MODE_OFB, iv=iv)
    # global iv
    # iv = cipher.iv
    encrypted = cipher.encrypt(byte_arrayed_token_block)
    nibblated, unnibblated_token = post_encryption(encrypted)
    # print(nibblated)

    # interfacing
    return nibblated

    # return unnibblated_token

# interfacing
# encrypted_token_20digits = encrypt(token_block, decoder_key)
# print(encrypted_token_20digits)

#################
# METER OPS BELOW
#################


def pre_decryption(token_20digits):
    token_bits66 = bin_pad(bin_str(int(token_20digits)), 66)
    exploded_token_bits = [i for i in token_bits66]
    i_28_27 = exploded_token_bits[0:2]
    exploded_token_bits[-29] = i_28_27[0]
    exploded_token_bits[-28] = i_28_27[1]
    exploded_token_bits.pop(0)
    exploded_token_bits.pop(0)

    concatenated_key = reduce(concat_str, exploded_token_bits)
    return concatenated_key


def decrypt(token_20digits):
    class_removed = pre_decryption(token_20digits)
    class_removed_int = int(class_removed, base=2)
    class_removed_hex_padded = bin_pad(hex(class_removed_int).lstrip('0x'), 16)
    byte_arrayed_token = bytearray.fromhex(class_removed_hex_padded)

    decoder_key_int = int(decoder_key, base=2)
    decoder_key_hex_padded = bin_pad(hex(decoder_key_int).lstrip('0x'), 16)
    byte_arrayed_decoder_key = bytearray.fromhex(decoder_key_hex_padded)

    cipher = DES.new(byte_arrayed_decoder_key, DES.MODE_OFB, iv=iv)
    decrypted = cipher.decrypt(byte_arrayed_token)

    token_block_bin = bin_pad(bin_str(int(decrypted.hex(), base=16)), 64)

    return token_block_bin

# interfacing
# decrypted_token = decrypt(encrypted_token_20digits)


def extract_token_info(decrypted_token):
    subclass = decrypted_token[0: 4]
    rnd_bits = decrypted_token[4: 8]

    tk_id = decrypted_token[8: 32]
    tk_id_formatted = base_date + \
        timedelta(minutes=int(decrypted_token[8: 32], base=2))

    amount = decrypted_token[32: 48]
    amount_formatted = int(decrypted_token[32: 48], base=2)

    token_order = [token_class, subclass, rnd_bits, tk_id, amount]
    crc_data = reduce(concat_str, token_order)
    crc = {'received': decrypted_token[48:], 'calculated': crc16(crc_data)}

    token_info = {
        'class': token_class,
        'subclass': subclass,
        'rnd': rnd_bits,
        'tkid': tk_id_formatted,
        'amount': amount_formatted,
        'crc': crc
    }
    # print(token_info)
    return token_info

# token_info = extract_token_info(decrypted_token)


# nibblated = encrypt(token_block, decoder_key)

# 'priceGross': ,
# 'priceNet': ,
# 'debt': ,
# 'vat': ,
# token_gen_response = f"""{{
#     'token': {nibblated},
#     'rate': {rate}
# }}"""
# print(
# token_gen_response
# )


# print(str(nibblated))


if __name__ == "__main__":
    import sys

    rate = sys.argv[1]
    amount = sys.argv[2]
    meter_number = sys.argv[3]
    token_class = sys.argv[4] # [0-3]
    token_subclass = sys.argv[5] # [0-15]

    token_block = generate_token_block(float(rate), int(amount), int(token_class), int(token_subclass))
    decoder_key = generate_decoder_key(int(meter_number))

    nibblated = encrypt(token_block, decoder_key)
    #

    print(nibblated)
