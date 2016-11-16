def read_and_check(file):
    magic = read(file)
    check(magic)
    return magic


def read(file):
    return file.read_unit32()


def check(magic):
    if magic != 0xcafebabe:
        raise
