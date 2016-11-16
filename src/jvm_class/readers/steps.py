def read(file):
    magic = read_and_check_magic(file)
    version = read_and_check_version(file)
    constant = read_constant_pool(file)
    access_flags = read_access_flags(file)
    this_class = read_this_class(file)
    super_class = read_super_class(file)
    interfaces = read_interfaces(file)
    fields = read_fields(file)
    methods = read_methods(file)
    attributes = read_attributes(file)


# step 1
def read_and_check_magic(file):
    magic = file.read_unit32()
    if magic == 0xcafebabe:
        return magic
    else:
        raise


# step 2
def read_and_check_version(file):
    minor_version = file.read_unit16()
    major_version = file.read_unit16()
    major_45 = (major_version == 45)
    major_46_to_52 = (major_version in range(46, 53) and
                      minor_version == 0)
    if major_45 or major_46_to_52:
        return major_version, minor_version
    else:
        raise


# step 3
def read_constant_pool(file):
    pass


# step 4
def read_access_flags(file):
    access_flags = file.read_unit16()
    return access_flags


# step 5
def read_this_class(file):
    this_class = file.read_unit16()
    return this_class


# step 6
def read_super_class(file):
    super_class = file.read_unit16()
    return super_class


# step 7
def read_interfaces(file):
    interfaces = file.read_unit16s()
    return interfaces


# step 8
def read_fields(file):
    pass


# step 9
def read_methods(file):
    pass


# step 10
def read_attributes(file):
    pass
