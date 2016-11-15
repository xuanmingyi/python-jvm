import struct

from utils import panic

from attribute import Attribute, Code

class CONSTANT_Utf8(object):
    def __init__(self, string):
        self.string = string 


class CONSTANT_Class(object):
    def __init__(self, name_index):
        self.name_index = name_index


class CONSTANT_String(object):
    def __init__(self, string_index):
        self.string_index = string_index


class CONSTANT_Fieldref(object):
    def __init__(self, class_index, name_and_type_index):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index


class CONSTANT_Methodref(object):
    def __init__(self, class_index, name_and_type_index):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index


class CONSTANT_NameAndType(object):
    def __init__(self, name_index, descriptor_index):
        self.name_index = name_index
        self.descriptor_index = descriptor_index


class Method(object):
    def __init__(self, access_flags, name_index, descriptor_index, attributes_count):
        self.access_flags = access_flags
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.attributes_count = attributes_count
        self.attributes = []

class Class(object):
    def __init__(self, data):
        self.constant_maps = [
            self.constant_undefined,                #                               0
            self.constant_utf8,                     # CONSTANT_Utf8                 1
            self.constant_undefined,                #
            self.constant_integer,                  # CONSTANT_Integer              3
            self.constant_float,                    # CONSTANT_Float                4
            self.constant_long,                     # CONSTANT_Long                 5
            self.constant_double,                   # CONSTANT_Double               6
            self.constant_class,                    # CONSTANT_Class                7
            self.constant_string,                   # CONSTANT_String               8
            self.constant_fieldref,                 # CONSTANT_Fieldref             9
            self.constant_methodref,                # CONSTANT_Methodref            a
            self.constant_interface_methodref,      # CONSTANT_InterfaceMethodref   b
            self.constant_name_and_type,            # CONSTANT_NameAndType          c
        ]

        self.data = data
        self.size = 0

        self.magic = self.read_u4()
        self.minor_version = self.read_u2()
        self.major_version = self.read_u2()

        try:
            self.check_vaild()
        except:
            panic("invaild class file")

        self.constant_pool_count = self.read_u2()
        self.constant_pool = []

        for i in range(1, self.constant_pool_count):
            tag = self.read_u1()
            if tag < len(self.constant_maps):
                self.constant_maps[tag]()

        self.access_flags = self.read_u2()
        self.this_class = self.read_u2()
        self.super_class = self.read_u2()

        self.interfaces_count = self.read_u2()
        self.interfaces = []

        self.fields_count = self.read_u2()
        self.fields = []

        self.methods_count = self.read_u2()
        self.methods = []

        for i in range(self.methods_count):
            self.methods.append(self.read_mehtod())

        self.attributes_count = self.read_u2()
        self.attributes = []

        for i in range(self.attributes_count):
            self.attributes.append(self.read_attribute())


    def read_mehtod(self):
        access_flags = self.read_u2()
        name_index = self.read_u2()
        descriptor_index = self.read_u2()
        attributes_count = self.read_u2()
        method = Method(access_flags, name_index, descriptor_index, attributes_count)

        for i in range(attributes_count):
            method.attributes.append(self.read_attribute())

        return method

    def read_attribute(self):
        attribute_name_index = self.read_u2()
        attribute_length = self.read_u4()

        attribute_name = self.get_utf8(attribute_name_index)
        attributes = []

        if attribute_name == "Code":
            print "Code"
            max_stack = self.read_u2()
            mac_locals = self.read_u2()
            code_length = self.read_u4()
            code = self._read(">{0}s".format(code_length))
            exception_table_length = self.read_u2()
            # fix exception

            attributes_count = self.read_u2()
            for i in range(attributes_count):
                attributes.append(self.read_attribute())
        else:
            self._read(">{0}s".format(attribute_length))
        return None

    def constant_utf8(self):
        length = self.read_u2()
        data = self._read(">{0}s".format(length))
        self.constant_pool.append(CONSTANT_Utf8(data.encode("utf8")))

    def constant_undefined(self):
        raise

    def constant_integer(self):
        raise

    def constant_float(self):
        raise

    def constant_long(self):
        raise

    def constant_double(self):
        raise

    def constant_class(self):
        name_index = self.read_u2()
        self.constant_pool.append(CONSTANT_Class(name_index))

    def constant_string(self):
        string_index = self.read_u2()
        self.constant_pool.append(CONSTANT_String(string_index))

    def constant_fieldref(self):
        class_index = self.read_u2()
        name_and_type_index = self.read_u2()
        self.constant_pool.append(
            CONSTANT_Fieldref(class_index, name_and_type_index))

    def constant_methodref(self):
        class_index = self.read_u2()
        name_and_type_index = self.read_u2()
        self.constant_pool.append(
            CONSTANT_Methodref(class_index, name_and_type_index))

    def constant_interface_methodref(self):
        raise

    def constant_name_and_type(self):
        name_index = self.read_u2()
        descriptor_index = self.read_u2()
        self.constant_pool.append(
            CONSTANT_NameAndType(name_index, descriptor_index))

    def get_utf8(self, index):
        ob = self.constant_pool[index - 1]
        if isinstance(ob, CONSTANT_Utf8):
            return self.constant_pool[index - 1].string
        elif isinstance(ob, CONSTANT_String):
            return self.get_utf8(ob.string_index)
        else:
            raise

    # check func

    def check_vaild(self):
        if self.magic != 0xcafebabe:
            raise
        if not self.check_version():
            raise

    def check_version(self):
        if self.major_version== 45:
            return True
        if self.major_version in [46, 47, 48, 49, 50, 51, 52] and\
           self.minor_version == 0:
            return True
        return False

    # inline read func

    def _read(self, _s):
        s = struct.Struct(_s)
        (data, ) = s.unpack(self.data[self.size:self.size+s.size])
        self.size += s.size
        return data

    def read_u1(self):
        return self._read(">B")

    def read_u2(self):
        return self._read(">H")

    def read_u4(self):
        return self._read(">I")
