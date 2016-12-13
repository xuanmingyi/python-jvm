from . import steps


def read(file):
    magic = steps.read_and_check_magic(file)
    version = steps.read_and_check_version(file)
    constants_pool = steps.read_constants_pool(file)
    access_flags = steps.read_access_flags(file)
    this_class = steps.read_this_class(file, constants_pool)
    super_class = steps.read_super_class(file, constants_pool)
    interfaces = steps.read_interfaces(file, constants_pool)
    fields = steps.read_fields(file, constants_pool)
    methods = steps.read_methods(file)
    attributes = steps.read_attributes(file)
    return {
        "magic": magic,
        "version": version,
        "constants_pool": constants_pool,
        "access_flags": access_flags,
        "this_class": this_class,
        "super_class": super_class,
        "interfaces": interfaces,
        "fields": fields,
        "methods": methods,
        "attributes": attributes
    }
