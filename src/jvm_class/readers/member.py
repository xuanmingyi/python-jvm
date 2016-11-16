from collections import namedtuple


Member = namedtuple('Member', ['access_flags',
                               'name_index',
                               'name',
                               'descriptor_index',
                               'attributes'])


def read_members(file, pool):
    size = file.read_unit16()
    members = [read_member(file, pool) for i in range(size)]
    return members


def read_member(file, pool):
    access_flags = file.read_unit16()
    name_index = file.read_unit16()
    descriptor_index = file.read_unit16()
    attributes = read_attributes(file, pool)

    name = pool.get_utf8(name_index)
    descriptor = pool.get_utf8(descriptor_index)

    return Member(access_flags=access_flags,
                  name_index=name_index,
                  name=name,
                  descriptor_index=descriptor_index,
                  descriptor=descriptor,
                  attributes=attributes)


def read_attributes(file, pool):
    pass
