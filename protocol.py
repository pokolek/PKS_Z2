# riesenie bolo inspirovanie https://github.com/iamhimanshu0/CRC/blob/master/CRC.py
message_type = {
    'ACK': '0',
    'RST': '1',
    'KPA': '2',
    'PSH': '3',
    'I_FILE': '4',
    'I_MSG': '5',
    'FIN': '6'
}

header_size = 6


class ProtocolHeader:
    def __init__(self, msg_tpe, size, checksum):
        self.msg_tpe = msg_tpe
        self.size = size
        self.checksum = checksum


def sum_checksum(checksum):
    """ Count all bits from given checksum. Return string of this count.

    checksum: Computed checksum to sum all bits. """

    sum_digit = 0
    for char in checksum:
        if char.isdigit():
            sum_digit += int(char)
    return str(sum_digit)


def xor(a, b):
    """ Logical XOR method for CRC. Returns string of bits.
    a XOR b

    a: Bit number for XOR.
    b: Bit number for XOR. """

    result = []  # initialize result
    for i in range(1, len(b)):  # go through all bits
        if a[i] == b[i]:  # same - XOR is 0
            result.append('0')
            continue
        result.append('1')  # not same - XOR is 1
    return ''.join(result)


def set_crc(data):
    """ Get checksum based on CRC method. Returns summary of all checksum bits as string.

     data: Data for CRC. """
    key = '1001'
    crc_key_len = len(key)
    bin_data = (''.join(format(ord(char), 'b') for char in str(data))) + ('0' * (crc_key_len - 1))
    checksum = bin_data[:crc_key_len]
    while crc_key_len < len(bin_data):
        if checksum[0] == '1':
            checksum = xor(key, checksum) + bin_data[crc_key_len]
        else:
            checksum = xor('0' * crc_key_len, checksum) + bin_data[crc_key_len]
        crc_key_len += 1
    if checksum[0] == '1':
        checksum = xor(key, checksum)
    else:
        checksum = xor('0' * crc_key_len, checksum)
    # print("check: ", str(checksum), data)
    return sum_checksum(checksum)
