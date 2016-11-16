import types


def bound_methods(obj, methods):
    for name, method in methods.items():
        method = types.MethodType(method, obj)
        setattr(obj, name, method)

    return obj


def class_file_methods():
    def read_unit8(self):
        return self.file.read(8)

    def read_unit16(self):
        return self.file.read(16)

    def read_unit32(self):
        return self.file.read(32)

    def read_unit64(self):
        return self.file.read(64)

    def read_u1(self):
        return self.read_unit8()

    def read_u2(self):
        return self.read_unit16()

    def read_u4(self):
        return self.read_unit32()

    def read_unit16s(self):
        length = self.read_unit16()
        return [self.read_unit16() for i in range(length)]

    return locals()


def class_file(file):
    methods = class_file_methods()
    file = bound_methods(file, methods)
    return file


def class_struct(file):
    def read_and_check_magic(file):
        magic = file.read_unit32()
        if magic == 0xcafebabe:
            return magic
        else:
            raise

    def read_and_check_version(file):
        minor_version = file.read_unit16()
        major_version = file.read_unit16()
        major_45 = (major_version == 45)
        major_46_to_52 = (major_version in range(46, 53) and
                          minor_version == 0)
        if not major_45 and not major_46_to_52:
            raise

    file = class_file(file)







class Class(object):
    __slots__ = ('minor_version',
                 'major_version',
                 'constant_pool',
                 'access_flags',
                 'this_class',
                 'super_class',
                 'inferfaces',
                 'fileds',
                 'methods',
                 'attributes')

    def __init__(self, data):
        with read(data) as class_file:
            def read_and_check_magic():
                magic = class_file.read_unit32()
                if magic != 0xcafebabe:
                    raise

            def read_and_check_version():
                self.minor_version = class_file.read_unit16()
                self.major_version = class_file.read_unit16()
                major_45 = (self.major_version == 45)
                major_46_to_52 = (self.major_version in range(46, 53) and
                                  self.minor_version == 0)
                if not major_45 and not major_46_to_52:
                    raise

            # def read_and_check_version():
            #     minor_version = class_file.read_unit16()
            #     major_version = class_file.read_unit16()

            #     if major_version == 45:
            #         self.major_version = major_version
            #         self.minor_version = minor_version
            #     elif major_version in range(46, 53) and minor_version == 0:
            #         self.major_version = major_version
            #         self.minor_version = minor_version
            #     else:
            #         raise

            def read_and_check_version():
                self.minor_version = class_file.read_unit16()
                self.major_version = class_file.read_unit16()
                major_45 = (self.major_version == 45)
                major_46_to_52 = (self.major_version in range(46, 53) and
                                  self.minor_version == 0)
                if not major_45 and not major_46_to_52:
                    raise

            def read_constant_pool():
                size = class_file.read_unit16()


            self.minor_version = 1
            self.major_version = 2
            self.constant_pool = 3
            self.access_flags = 4
            self.this_class = 5
            self.super_class = 6
            self.inferfaces = []
            self.fileds = []
            self.methods = []
            self.attributes = []


class Structs(object):
    pass
