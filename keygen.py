from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes


def generate_vending_key():
    vending_key = get_random_bytes(8)
    # vending_key = b'\xee\x11Z{\t\x96\x0e\x11'
    return vending_key


def generate_decoder_key():

    # control block params
    key_type = 2  # [0-3]
    supply_group_code = 140152  # 6 digit <random>
    tariff_index = 11  # 2 digit
    key_revision_no = 1  # [1-9]
    pad_value = 'ffffff'  # 6 0xF s
    stringed_control_params = list(map(lambda x: str(x), [key_type, supply_group_code, tariff_index, key_revision_no, pad_value]))

    # pan block params
    issuer_id_no = 600727  # sts specified
    decoder_reg_no = 35666666666  # random meter number
    stringed_pan_params = list(map(lambda x: str(x), [issuer_id_no, decoder_reg_no]))

    # blocks
    control_block = ''.join(stringed_control_params)
    pan_block = ''.join(stringed_pan_params)[-16:-1]

    # vending key
    vending_key = generate_vending_key()


    ##################
    # DKGA02 START
    ##################

    # 1
    x_1 = int(control_block, base=16) ^ int(pan_block, base=16)

    # 2
    hexed_x_1 = hex(x_1).lstrip('0x')
    byte_arrayed_x_1 = bytearray.fromhex(hexed_x_1)
    cipher = DES.new(vending_key, DES.MODE_OFB)
    secret = cipher.encrypt(byte_arrayed_x_1)

    # 3
    inted_secret = int(secret.hex(), base=16)
    x_2 = x_1 ^ inted_secret

    # 4
    inted_vending_key = int(vending_key.hex(), base=16)
    x_3 = x_2 ^ inted_vending_key

    # 5
    decoder_key = hex(x_3)

    ##################
    # DKGA02 END
    ##################

    return decoder_key