from . import base, constant, member


# step 1
def read_and_check_magic(file):
    magic = base.read_int32(file)
    if magic == 0xcafebabe:
        return magic
    else:
        raise Exception("magic should be {}, rather than {}".format(0xcafebabe, magic))


# step 2
def read_and_check_version(file):
    minor_version = base.read_int16(file)
    major_version = base.read_int16(file)
    major_45 = (major_version == 45)
    major_46_to_52 = (major_version in range(46, 53) and
                      minor_version == 0)
    if major_45 or major_46_to_52:
        return major_version, minor_version
    else:
        raise Exception("major version should be 45 or range(46, 53), rather than {}".format(major_version))


# step 3
def read_constants_pool(file):
    return constant.read_constants_pool(file)


# step 4
def read_access_flags(file):
    access_flags = base.read_unit16(file)
    return access_flags


# step 5
def read_this_class(file, pool):
    index = base.read_int16(file)
    return pool.get_class(index)


# step 6
def read_super_class(file, pool):
    index = base.read_int16(file)
    return pool.get_class(index)


# step 7
def read_interfaces(file, pool):
    indexs = base.read_indexs(file)
    return [pool.get_interface(index) for index in indexs]


# step 8
def read_fields(file, pool):
    return member.read_members(file, pool)


# step 9
def read_methods(file):
    pass


# step 10
def read_attributes(file):
    pass
