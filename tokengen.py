from functools import reduce
import random
import numpy as np

from datetime import datetime


base_date = datetime(2022, 4, 17)
rate = 3/200
amount_cash = 2000
utility_amount = rate * amount_cash
complimented_amount = int(utility_amount * 10)



def bin_str(int):
    return bin(int).lstrip('0b')

def concat_str(bin1, bin2, sep=''):
    return sep.join([bin1, bin2])

def bin_pad(binary, length: int):
    binary = str(binary)
    binary_length = len(binary)
    while binary_length < length:
        binary = '0' + binary 
        binary_length += 1
    return binary


token_class = bin_pad(bin_str(0), 2) #[0-3]
token_subclass = bin_pad(bin_str(0), 4) #[0-15]

def crc16(data: str):
    '''
    CRC-16-ModBus Algorithm
    '''
    inted_data = int(data, base=2)
    hexed_data = hex(inted_data).lstrip('0x')
    bin_padded_hexed_data = bin_pad(hexed_data, 14)
    data = bytearray.fromhex(bin_padded_hexed_data)
    # poly = 0x8404
    # poly = 0x18005
    poly = 0xA001

    # crc = 0x0000
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)
    
    # reverse byte order if you need to
    # crc = (crc << 8) | ((crc >> 8) & 0xFF)
    
    crc = int(np.uint16(crc))
    return bin_pad(bin_str(crc), 16)


def get_exponent(amount: int):
    exponent = 3
    if amount <= 16383:
        exponent = 0
    elif amount <= 180214:
        exponent = 1
    elif amount <= 1818524:
        exponent = 2

    return exponent

def get_mantissa(exponent: int, amount: int):
    if exponent == 0:
        return bin_pad(bin_str(amount), 14)
    else:
        rhs_sum = 0
        for i in range(1, exponent + 1):
            rhs_sum += int(2**14 * 10^(i-1))

    mantissa = (amount - rhs_sum) / int(10 ** exponent)
    return bin_pad(bin_str(mantissa), 14)

def get_random(): # TBD 4 DP
    rnd = random.randint(0, 15)
    return bin_pad(bin_str(rnd), 4)

def get_token_id():
    now = datetime.now()
    delta = now - base_date
    minutes_from_base_date = int(delta.total_seconds() / 60)
    return bin_pad(bin_str(minutes_from_base_date), 24)

exponent = get_exponent(complimented_amount)
dressed_exponent = bin_pad(bin_str(exponent), 2)
def get_amount_block():
    mantissa = get_mantissa(exponent, complimented_amount)
    amount_block = concat_str(bin_pad(bin_str(exponent), 2), bin_pad(bin_str(mantissa), 14))
    return amount_block


def generate_token_block():
    token_order = [token_class, token_subclass, get_random(), get_token_id(), dressed_exponent, get_mantissa(exponent, complimented_amount)]
    crc = crc16(reduce(concat_str, token_order))
    token_order.append(crc)
    token64_order = token_order[1:]
    return reduce(concat_str, token64_order)
