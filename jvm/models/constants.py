from enum import Enum


class Pool(dict):
    def get(self, index):
        if index in self:
            return self[index]
        else:
            raise Exception("{} is invalid".format(index))

    def get_utf8(self, index):
        utf8 = self.get(index)
        if isinstance(utf8, UTF8):
            return utf8
        else:
            raise Exception("{} should be UTF8, rather than {}".format(index, self.get(index)))

    def get_name_and_type(self, index):
        name_and_type = self.get(index)
        if isinstance(name_and_type, NameAndType):
            return name_and_type
        else:
            raise Exception("{} should be NameAndType, rather than {}".format(index, self.get(index)))

    def get_class(self, index):
        jvm_class = self.get(index)
        if isinstance(jvm_class, Class):
            return jvm_class
        else:
            raise Exception("{} should be Class, rather than {}".format(index, self.get(index)))

    def get_interface(self, index):
        interface = self.get(index)
        if isinstance(interface, InterfaceMethodred):
            return interface
        else:
            raise Exception("{} should be InterfaceMethodred, rather than {}".format(index, self.get(index)))


class Tags(Enum):
    UTF8 = 1
    Interger = 3
    Float = 4
    Long = 5
    Double = 6
    Class = 7
    String = 8
    Fieldref = 9
    Methodref = 10
    InterfaceMethodref = 11
    NameAndType = 12
    MethodHandle = 15
    MethodType = 16
    InvokeDynamic = 18


class Constant(object):
    def __init__(self, pool, value):
        self.pool = pool
        self.value = value


class UTF8(Constant):
    tag = Tags.UTF8

    def __repr__(self):
        return "<UTF8: \"{}\">".format(self.value)


class Interger(Constant):
    tag = Tags.Interger

    def __repr__(Interger):
        return "<Interger: {}>".format(self.value)


class Float(Constant):
    tag = Tags.Float

    def __repr__(self):
        return "<Float: {}>".format(self.value)


class Long(Constant):
    tag = Tags.Long

    def __repr__(self):
        return "<Long: {}>".format(self.value)


class Double(Constant):
    tag = Tags.Double

    def __repr__(self):
        return "<Double: {}>".format(self.value)


class Class(Constant):
    tag = Tags.Class

    def __repr__(self):
        return "<Class: {}>".format(self.name)

    def __init__(self, pool, name_index):
        self.pool = pool
        self.name_index = name_index

    @property
    def name(self):
        return self.pool.get_utf8(self.name_index).value


class String(Constant):
    tag = Tags.String

    def __repr__(self):
        return "<String: \"{}\">".format(self.value)

    def __init__(self, pool, index):
        self.pool = pool
        self.index = index

    @property
    def value(self):
        return self.pool.get_utf8(self.index).value


class NameAndType(Constant):
    tag = Tags.NameAndType

    def __repr__(self):
        return ("<NameAndType: (Name: {}, Type: {})"
               ).format(self.name , self.type)

    def __init__(self, pool, name_index, descriptor_index):
        self.pool = pool
        self.name_index = name_index
        self.descriptor_index = descriptor_index

    @property
    def name(self):
        return self.pool.get_utf8(self.name_index).value

    @property
    def type(self):
        return self.pool.get_utf8(self.descriptor_index).value


class Ref(Constant):
    def __init__(self, pool, class_index, name_and_type_index):
        self.pool = pool
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    @property
    def jvm_class(self):
        return self.pool.get_class(self.class_index)

    @property
    def name_and_type(self):
        return self.pool.get_name_and_type(self.name_and_type_index)

    @property
    def name(self):
        return self.name_and_type.name

    @property
    def type(self):
        return self.name_and_type.type


class Fieldref(Ref):
    tag = Tags.Fieldref

    def __repr__(self):
        return ("<Fieldref: (Class: {}, Name: {}, Type: {})"
               ).format(self.jvm_class.name, self.name, self.type)


class Methodref(Ref):
    tag = Tags.Methodref

    def __repr__(self):
        return ("<Methodref: (Class: {}, Name: {}, Type: {})"
               ).format(self.jvm_class.name, self.name, self.type)


class InterfaceMethodred(Ref):
    tag = Tags.InterfaceMethodref

    def __repr__(self):
        return ("<InterfaceMethodred: (Class: {}, Name: {}, Type: {})"
               ).format(self.jvm_class.name, self.name, self.type)
