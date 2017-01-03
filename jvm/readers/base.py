from . import utils


def read(file, length):
    return file.read(length)


def read_unit8(file):
    return read(file, 1)


def read_unit16(file):
    return read(file, 2)


def read_unit32(file):
    return read(file, 4)


def read_unit64(file):
    return read(file, 8)


def read_u1(file):
    return read_unit8(file)


def read_u2(file):
    return read_unit16(file)


def read_u4(file):
    return read_unit32(file)


def read_unit16s(file):
    length = read_int16(file)
    return [read_unit16(file) for i in range(length)]


def read_int8(file):
    bytes = read_unit8(file)
    return utils.bytes_to_int(bytes)


def read_int16(file):
    bytes = read_unit16(file)
    return utils.bytes_to_int(bytes)


def read_int32(file):
    bytes = read_unit32(file)
    return utils.bytes_to_int(bytes)


def read_int64(file):
    bytes = read_unit64(file)
    return utils.bytes_to_int(bytes)


def read_interger8(file):
    bytes = read_unit8(file)
    return utils.bytes_to_int(bytes, signed=True)


def read_interger(file):
    bytes = read_unit32(file)
    return utils.bytes_to_int(bytes, signed=True)


def read_long(file):
    bytes = read_unit64(file)
    return utils.bytes_to_int(bytes, signed=True)


def read_float32(file):
    bytes = read_unit32(file)
    return utils.bytes_to_float(bytes)


def read_float64(file):
    bytes = read_unit64(file)
    return utils.bytes_to_float(bytes)


def read_float(file):
    return read_float32(file)


def read_double(file):
    return read_float64(file)


def read_index(file):
    return read_int16(file)


def read_indexs(file):
    length = read_int16(file)
    return [read_index(file) for i in range(length)]


def read_string(file):
    length = read_int16(file)
    bytes = file.read(length)
    return bytes.decode('utf-8')
