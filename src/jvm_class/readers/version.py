def read_and_check(file):
    major_version, minor_version = read(file)
    check(major_version, minor_version)
    return major_version, minor_version


def read(file):
    minor_version = file.read_unit16()
    major_version = file.read_unit16()
    return major_version, minor_version


def check(major_version, minor_version):
    major_45 = (major_version == 45)
    major_46_to_52 = (major_version in range(46, 53) and
                      minor_version == 0)
    if not major_45 and not major_46_to_52:
        raise
