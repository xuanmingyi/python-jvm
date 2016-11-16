import sys

from enum import Enum
from collections import namedtuple


def read_constant_pool(file):
    pool = {}

    size = file.read_unit16()
    size = int.from_bytes(size, byteorder=sys.byteorder, signed=True)

    index = 1
    while index < size:
        constant, constant_size = read_constant(file, pool)
        pool[index] = constant
        index += constant_size

    return pool


def read_constant(file, pool):
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

    ReadNeedPool = (Tags.Class, Tags.String, Tags.Fieldref, Tags.NameAndType)
    LargeSizeType = (Tags.Long, Tags.Double)

    read = ConstantMap.get(tag)

    if read:
        constant = read(file, pool) if tag in ReadNeedPool else read(file)
        size = 2 if tag in LargeSizeType else 1
        return constant, size
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


Interger = namedtuple('Interger', ['value'])
Float = namedtuple('Float', ['value'])
Long = namedtuple('Long', ['value'])
Double = namedtuple('Double', ['value'])
UTF8 = namedtuple('UTF8', ['value'])
String = namedtuple('String', ['index', 'value'])
Class = namedtuple('Class', ['name_index', 'name'])
NameAndType = namedtuple('NameAndType', ['name_index', 'name',
                                         'descriptor_index', 'descriptor'])
Fieldref = namedtuple('Fieldref', ['class_index', 'class_name',
                                   'name_and_type_index', 'name_and_type'])
Methodref = namedtuple('Methodref', ['class_index', 'class_name',
                                     'name_and_type_index', 'name_and_type'])
InterfaceMethodref = namedtuple('InterfaceMethodref', ['class_index',
                                                       'class_name',
                                                       'name_and_type_index',
                                                       'name_and_type'])


def get_interger(file):
    value = file.read_unit32()
    value = int.from_bytes(value, byteorder=sys.byteorder, signed=True)
    return Interger(value=value)


def get_float(file):
    value = file.read_unit32()
    value = float.fromhex(value)
    return Float(value=value)


def get_long(file):
    value = file.read_unit64()
    value = int.from_bytes(value, byteorder=sys.byteorder, signed=True)
    return Long(value=value)


def get_double(file):
    value = file.read_unit64()
    value = float.fromhex(value)
    return Double(value=value)


def get_utf8(file):
    length = file.read_unit16()
    value = file.read(length)
    value = value.decode('utf-8')
    return UTF8(value=value)


def get_string(file, pool):
    index = file.read_unit16()

    value = pool.get_utf8(index)

    return String(index=index, value=value)


def get_class(file, pool):
    name_index = file.read_unit16()

    name = pool.get_utf8(name_index)

    return Class(name_index=name_index, name=name)


def get_name_and_type(file, pool):
    name_index = file.read_unit16()
    descriptor_index = file.read_unit16()

    name = pool.get_utf8(name_index)
    descriptor = pool.get_utf8(descriptor_index)

    return NameAndType(name_index=name_index,
                       name=name,
                       descriptor_index=descriptor_index,
                       descriptor=descriptor)


def get_fieldref(file, pool):
    class_index = file.read_unit16()
    name_and_type_index = file.read_unit16()

    class_name = pool.get_class_name(class_index)
    name_and_type = pool.get_name_and_type(name_and_type_index)

    return Fieldref(class_index=class_index,
                    class_name=class_name,
                    name_and_type_index=name_and_type_index,
                    name_and_type=name_and_type)


def get_methodref(file, pool):
    class_index = file.read_unit16()
    name_and_type_index = file.read_unit16()

    class_name = pool.get_class_name(class_index)
    name_and_type = pool.get_name_and_type(name_and_type_index)

    return Methodref(class_index=class_index,
                     class_name=class_name,
                     name_and_type_index=name_and_type_index,
                     name_and_type=name_and_type)


def get_interface_methodref(file, pool):
    class_index = file.read_unit16()
    name_and_type_index = file.read_unit16()

    class_name = pool.get_class_name(class_index)
    name_and_type = pool.get_name_and_type(name_and_type_index)

    return InterfaceMethodref(class_index=class_index,
                              class_name=class_name,
                              name_and_type_index=name_and_type_index,
                              name_and_type=name_and_type)


def get_method_handle(file):
    raise


def get_method_type(file):
    raise


def get_invoke_dynamic(file):
    raise
