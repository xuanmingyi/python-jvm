from collections import namedtuple
from . import base, attributes


def read_members(file, pool):
    size = base.read_int16(file)
    members = [read_member(file, pool) for i in range(size)]
    return members


def read_member(file, pool):
    access_flags = file.read_unit16()
    name_index = file.read_index()
    descriptor_index = file.read_index()
    attributes = attributes.read_attributes(file, pool)
    return access_flags, name_index, descriptor_index, attributes
