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


# riesenie bolo inspirovanie https://github.com/iamhimanshu0/CRC/blob/master/CRC.py
def xor(a, b):
    result = []
    # prechadzame po bitoch
    for i in range(1, len(b)):
        # XOR je 0 ak su rovnake
        if a[i] == b[i]:
            result.append('0')
        # XOR je 1 ked su rozne
        else:
            result.append('1')
    return ''.join(result)


# riesenie bolo inspirovanie https://github.com/iamhimanshu0/CRC/blob/master/CRC.py
def get_checksum(data):
    key = '1101'
    crc_key_len = len(key)

    # prevedenie do binarneho tvaru
    binary_form = ''
    for char in str(data):
        binary_form += (format(ord(char), 'b'))
    binary_form += ('0' * (4 - 1))
    checksum = binary_form[:crc_key_len]
    while crc_key_len < len(binary_form):
        if checksum[0] == '1':
            checksum = xor(key, checksum) + binary_form[crc_key_len]
        else:
            checksum = xor('0' * crc_key_len, checksum) + binary_form[crc_key_len]
        crc_key_len += 1
    if checksum[0] == '1':
        checksum = xor(key, checksum)
    else:
        checksum = xor('0' * crc_key_len, checksum)

    sum_digit = 0
    for char in checksum:
        if char.isdigit():
            sum_digit += int(char)
    return str(sum_digit)
