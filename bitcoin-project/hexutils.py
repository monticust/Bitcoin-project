import binascii


def hexprint(byte_array):
    print(binascii.hexlify(byte_array, b" "))