def bytes_to_int(bytes, signed=False):
    return int.from_bytes(bytes, byteorder='big', signed=signed)


def bytes_to_float(bytes):
    return float.fromhex(bytes)
