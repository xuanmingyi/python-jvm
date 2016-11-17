import sys

from enum import Enum


def read_constant_pool(file):
    pool = {}

    size = file.read_unit16()
    size = int.from_bytes(size, byteorder=sys.byteorder, signed=True)

    index = 1
    while index < size:
        constant, constant_size = read_constant(file, pool)
        pool[index] = constant
        index += constant_size

    pool = make_cache(pool)

    return pool


def read_constant(file):
    tag = file.read_unit8()
    tag = int.from_bytes(tag, byteorder=sys.byteorder, signed=True)

    ConstantMap = {
        Tags.UTF8: get_utf8,
        Tags.Interger: get_interger,
        Tags.Float: get_float,
        Tags.Long: get_long,
        Tags.Double: get_double,
        Tags.Class: get_class,
        Tags.String: get_string,
        Tags.Fieldref: get_fieldref,
        Tags.NameAndType: get_name_and_type,
        Tags.MethodHandle: get_method_handle,
        Tags.MethodType: get_method_type,
        Tags.InvokeDynamic: get_invoke_dynamic,
    }

    LargeSizeType = (Tags.Long, Tags.Double)

    read = ConstantMap.get(tag)

    if read:
        constant = read(file)
        constant['tag'] = tag
        size = 2 if tag in LargeSizeType else 1
        return constant, size
    else:
        raise


def make_cache(pool):
    for index, constant in pool.items():
        pool[index] = make_constant_cache(constant, pool)
    return pool


def make_constant_cache(constant, pool):
    if constant['tag'] == Tags.String:
        constant['value'] = get_utf8_from_pool(pool, constant['index'])
        return constant
    elif constant['tag'] in (Tags.Class, Tags.Fieldref, Tags.NameAndType):
        index_suffix = '_index'
        for key, value in constant.items():
            if key.endswith(index_suffix):
                name = key[:-len(index_suffix)]
                constant[name] = get_utf8_from_pool(pool, value)
        return constant
    else:
        return constant


def get_utf8_from_pool(pool, index):
    constant_utf8 = pool[index]
    if constant_utf8:
        return constant_utf8['value']
    else:
        raise


class Tags(Enum):
    UTF8 = 1
    Interger = 3
    Float = 4
    Long = 5
    Double = 6
    Class = 7
    String = 8
    Fieldref = 9
    NameAndType = 12
    MethodHandle = 15
    MethodType = 16
    InvokeDynamic = 18


def get_interger(file):
    value = file.read_unit32()
    value = int.from_bytes(value, byteorder=sys.byteorder, signed=True)
    return {'value': value}


def get_float(file):
    value = file.read_unit32()
    value = float.fromhex(value)
    return {'value': value}


def get_long(file):
    value = file.read_unit64()
    value = int.from_bytes(value, byteorder=sys.byteorder, signed=True)
    return {'value': value}


def get_double(file):
    value = file.read_unit64()
    value = float.fromhex(value)
    return {'value': value}


def get_utf8(file):
    length = file.read_unit16()
    value = file.read(length)
    value = value.decode('utf-8')
    return {'value': value}


def get_string(file):
    index = file.read_unit16()
    return {'index': index}


def get_class(file):
    name_index = file.read_unit16()
    return {'name_index': name_index}


def get_name_and_type(file):
    name_index = file.read_unit16()
    descriptor_index = file.read_unit16()
    return {'name_index': name_index, 'descriptor_index': descriptor_index}


def get_fieldref(file):
    class_index = file.read_unit16()
    name_and_type_index = file.read_unit16()
    return {
        'class_index': class_index,
        'name_and_type_index': name_and_type_index
    }


def get_methodref(file):
    class_index = file.read_unit16()
    name_and_type_index = file.read_unit16()
    return {
        'class_index': class_index,
        'name_and_type_index': name_and_type_index
    }


def get_interface_methodref(file):
    class_index = file.read_unit16()
    name_and_type_index = file.read_unit16()
    return {
        'class_index': class_index,
        'name_and_type_index': name_and_type_index
    }


def get_method_handle(file):
    raise


def get_method_type(file):
    raise


def get_invoke_dynamic(file):
    raise
