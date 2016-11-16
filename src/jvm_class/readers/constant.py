import sys

from enum import Enum
from collections import namedtuple


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
NameAndType = namedtuple('NameAndType', ['name_index', 'descriptor_index'])
Fieldref = namedtuple('Fieldref', ['class_index', 'class_name',
                                   'name_and_type_index', 'name_and_type'])
Methodref = namedtuple('Methodref', ['class_index', 'class_name',
                                     'name_and_type_index', 'name_and_type'])
InterfaceMethodref = namedtuple('InterfaceMethodref', ['class_index',
                                                       'class_name',
                                                       'name_and_type_index',
                                                       'name_and_type'])


class Interger(object):
    @staticmethod
    def read(file):
        value = file.read_unit32()
        value = int.from_bytes(value, byteorder=sys.byteorder, signed=True)
        return Interger(value=value)


class Float(object):
    @staticmethod
    def read(file):
        value = file.read_unit32()
        value = float.fromhex(value)
        return Float(value=value)


class Long(object):
    @staticmethod
    def read(file):
        value = file.read_unit64()
        value = int.from_bytes(value, byteorder=sys.byteorder, signed=True)
        return Long(value=value)


class Double(object):
    @staticmethod
    def read(file):
        value = file.read_unit64()
        value = float.fromhex(value)
        return Double(value=value)


class UTF8(object):
    @staticmethod
    def read(file):
        length = file.read_unit16()
        value = file.read(length)
        value = value.decode('utf-8')
        return UTF8(value=value)


class String(object):
    @staticmethod
    def read(file, pool):
        index = file.read_unit16()
        value = pool.get_utf8(index)
        return String(index=index, value=value)


class Class(object):
    @staticmethod
    def read(file, pool):
        name_index = file.read_unit16()
        name = pool.get_utf8(name_index)
        return Class(name_index=name_index, name=name)


class NameAndType(object):
    @staticmethod
    def read(file):
        name_index = file.read_unit16()
        descriptor_index = file.read_unit16()
        return NameAndType(name_index=name_index,
                           descriptor_index=descriptor_index)


class Fieldref(object):
    @staticmethod
    def read(file, pool):
        class_index = file.read_unit16()
        name_and_type_index = file.read_unit16()
        class_name = pool.get_class_name(class_index)
        name_and_type = pool.get_name_and_type(name_and_type_index)
        return Fieldref(class_index=class_index,
                        class_name=class_name,
                        name_and_type_index=name_and_type_index,
                        name_and_type=name_and_type)


class Methodref(object):
    @staticmethod
    def read(file, pool):
        class_index = file.read_unit16()
        name_and_type_index = file.read_unit16()
        class_name = pool.get_class_name(class_index)
        name_and_type = pool.get_name_and_type(name_and_type_index)
        return Methodref(class_index=class_index,
                         class_name=class_name,
                         name_and_type_index=name_and_type_index,
                         name_and_type=name_and_type)


class InterfaceMethodref(object):
    @staticmethod
    def read(file, pool):
        class_index = file.read_unit16()
        name_and_type_index = file.read_unit16()
        class_name = pool.get_class_name(class_index)
        name_and_type = pool.get_name_and_type(name_and_type_index)
        return InterfaceMethodref(class_index=class_index,
                                  class_name=class_name,
                                  name_and_type_index=name_and_type_index,
                                  name_and_type=name_and_type)
