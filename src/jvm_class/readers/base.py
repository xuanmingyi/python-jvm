import types


def bound_methods(obj, methods):
    for name, method in methods.items():
        method = types.MethodType(method, obj)
        setattr(obj, name, method)

    return obj


def base_readers():
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
    methods = base_readers()
    file = bound_methods(file, methods)
    return file
