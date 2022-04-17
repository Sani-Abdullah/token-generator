from email.mime import base
import random
import numpy as np

from datetime import datetime


rate = 3/200
amount_cash = 2000
utility_amount = rate * amount_cash

token_class = 0 #[0-3]
token_subclass = 0 #[0-15]

def concat(bin1, bin2):
    bin1 = bin1.lstrip('0b')
    bin2 = bin2.lstrip('0b')
    return ''.join([bin1, bin2])

def pad(binary, length: int):
    binary = str(binary)
    binary_length = len(binary)
    while binary_length < length:
        binary = '0' + binary 
        binary_length += 1
    print(binary)
    return binary

pad(11, 4)


def crc16(data: bytes):
    '''
    CRC-16-ModBus Algorithm
    '''
    data = bytearray(data)
    poly = 0x8404
    crc = 0x0000
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)
    
    # reverse byte order if you need to
    # crc = (crc << 8) | ((crc >> 8) & 0xFF)

    return np.uint16(crc)

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
        return amount
    else:
        rhs_sum = 0
        for i in range(1, exponent + 1):
            rhs_sum += int(2**14 * 10^(i-1))

    return (amount - rhs_sum) / int(10 ** exponent)

def get_random(): # TBD 4 DP
    return random.randint(0, 15)

def get_token_id():
    base_date = datetime(2022, 4, 17)
    now = datetime.now()
    delta = now - base_date
    minutes_from_base_date = int(delta.total_seconds() / 60)
    return minutes_from_base_date

def get_amount():
    complimented_amount = int(utility_amount * 10)
    exponent = pad(get_exponent(complimented_amount), 2)
    mantissa = get_mantissa(exponent, complimented_amount)
    amount_block = concat(bin(exponent), bin(mantissa))
    print(amount_block)

get_amount()