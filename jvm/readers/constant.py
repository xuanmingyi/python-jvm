from jvm.models.constants import (Tags,
                                  Pool,
                                  UTF8,
                                  Interger,
                                  Float,
                                  Long,
                                  Double,
                                  Class,
                                  String,
                                  Fieldref,
                                  NameAndType,
                                  Methodref,
                                  InterfaceMethodred)
from . import base


def read_constants_pool(file):
    pool = Pool()
    for index, constant in read_constants(file, pool):
        pool[index] = constant
    return pool


def read_constants(file, pool):
    size = base.read_int16(file)

    index = 1
    while index < size:
        constant, constant_size = read_constant(file, pool)
        yield index, constant
        index += constant_size


def read_constant(file, pool):
    tag = read_tag(file)
    read = get_read(tag)
    constant = read(file, pool)
    LargeSizeType = (Tags.Long, Tags.Double)
    size = 2 if tag in LargeSizeType else 1
    return constant, size


def get_read(tag):
    ConstantMap = {
        Tags.UTF8: get_utf8,
        Tags.Interger: get_interger,
        Tags.Float: get_float,
        Tags.Long: get_long,
        Tags.Double: get_double,
        Tags.Class: get_class,
        Tags.String: get_string,
        Tags.Fieldref: get_fieldref,
        Tags.Methodref: get_methodref,
        Tags.InterfaceMethodref: get_interface_methodref,
        Tags.NameAndType: get_name_and_type,
        Tags.MethodHandle: get_method_handle,
        Tags.MethodType: get_method_type,
        Tags.InvokeDynamic: get_invoke_dynamic,
    }
    return ConstantMap.get(Tags(tag))


# def make_cache(pool):
#     for index, constant in pool.items():
#         pool[index] = make_constant_cache(constant, pool)
#     return pool


# def make_constant_cache(constant, pool):
#     if constant['tag'] == Tags.String:
#         constant['value'] = get_utf8_from_pool(pool, constant['index'])
#         return constant
#     elif constant['tag'] in (Tags.Class, Tags.Fieldref, Tags.NameAndType):
#         index_suffix = '_index'
#         for key, value in constant.items():
#             if key.endswith(index_suffix):
#                 name = key[:-len(index_suffix)]
#                 constant[name] = get_utf8_from_pool(pool, value)
#         return constant
#     else:
#         return constant


# def get_utf8_from_pool(pool, index):
#     constant_utf8 = pool[index]
#     if constant_utf8:
#         return constant_utf8['value']
#     else:
#         raise Exception


def read_tag(file):
    return base.read_int8(file)


### readers


def get_interger(file, pool):
    value = base.read_interger(file)
    return Interger(pool, value)


def get_float(file, pool):
    value = base.read_float32(file)
    return Float(pool, value)


def get_long(file, pool):
    value = base.read_long(file)
    return Long(pool, value)


def get_double(file, pool):
    value = base.read_float64(file)
    return Double(pool, value)


def get_utf8(file, pool):
    value = base.read_string(file)
    return UTF8(pool, value)


def get_string(file, pool):
    index = base.read_index(file)
    return String(pool, index)


def get_class(file, pool):
    name_index = base.read_index(file)
    return Class(pool, name_index)


def get_name_and_type(file, pool):
    name_index = base.read_index(file)
    descriptor_index = base.read_index(file)
    return NameAndType(pool, name_index, descriptor_index)


def get_fieldref(file, pool):
    class_index = base.read_index(file)
    name_and_type_index = base.read_index(file)
    return Fieldref(pool, class_index, name_and_type_index)


def get_methodref(file, pool):
    class_index = base.read_index(file)
    name_and_type_index = base.read_index(file)
    return Methodref(pool, class_index, name_and_type_index)


def get_interface_methodref(file, pool):
    class_index = base.read_index(file)
    name_and_type_index = base.read_index(file)
    return InterfaceMethodred(pool, class_index, name_and_type_index)


def get_method_handle(file, pool):
    raise Exception


def get_method_type(file, pool):
    raise Exception


def get_invoke_dynamic(file, pool):
    raise Exception
