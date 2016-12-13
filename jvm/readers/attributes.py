from jvm.models.attributes import (Name,
                                   Unparsed,
                                   Deprecated,
                                   Synthetic,
                                   SourceFile,
                                   ConstantValue,
                                   Code,
                                   ExceptionTable,
                                   Exception,
                                   LineNumberTable,
                                   LineNumberTableEntry,
                                   LocalVariableTable,
                                   LocalVariableTableEntry)
from . import base


def read_attributes(file, pool):
    count = base.read_int16(file)
    return [read_attribute(file) for i in range(count)]


def read_attribute(file, pool):
    name_index = base.read_index(file)
    length = base.read_int32(file)

    name = pool.get_utf8(name_index).value
    read = get_read(name)
    return read(file, pool, name_index, length)


def get_read(name):
    AttributeMap = {
        Name.Code: read_code,
        Name.ConstantValue: read_constant_value,
        Name.Deprecated: read_deprecated,
        Name.Exceptions: read_exceptions,
        Name.LineNumberTable: read_line_number_table,
        Name.LocalVariableTable: read_local_variable_table,
        Name.SourceFile: read_source_file,
        Name.Synthetic: read_synthetic,
        Name.Unparsed: read_unparsed,
    }
    return AttributeMap.get(Name(name)) or get_unparsed


def read_code(file):
    pass


def read_unparsed(file, pool, name_index, length):
    info = base.read(file, length)
    return Unparsed(pool, name_index, length, info)


def read_deprecated(file, pool, name_index, length):
    return Deprecated(pool, name_index, length)


def read_synthetic(file, pool, name_index, length):
    return Synthetic(pool, name_index, length)


def read_source_file(file, pool, name_index, length):
    source_file_index = base.read_index(file)
    return SourceFile(pool, name_index, length, source_file_index)


def read_constant_value(file, pool, name_index, length):
    constant_value_index = base.read_index(file)
    return ConstantValue(pool, name_index, length, constant_value_index)


def read_code(file, pool, name_index, length):
    max_stack = base.read_int16(file)
    max_locals = base.read_int16(file)
    code_length = base.read_int32(file)
    code = base.read(code_length)
    exception_tables = read_exception_tables(file)
    attributes = read_attributes(file, pool)
    return Code(pool, name_index, length,
                max_stack, max_locals, code_length, code,
                exception_tables, attributes)


def read_exception_tables(file):
    length = base.read_int16()
    return [read_exception_table(file) for i in range(length)]


def read_exception_table(file):
    start_pc = base.read_int16(file)
    end_pc = base.read_int16(file)
    handler_pc = base.read_int16(file)
    catch_type = base.read_int16(file)
    return ExceptionTable(start_pc, end_pc, handler_pc, catch_type)


def read_exceptions(file, pool, name_index, length):
    exceptions = base.read_indexs(file)
    return Exception(pool, name_index, length, exceptions)


def read_line_number_table(file, pool, name_index, length):
    entry_length = base.read_int16(file)
    line_number_table = [read_line_number_table_entry(file)
                         for i in range(entry_length)]
    return LineNumberTable(line_number_table)


def read_line_number_table_entry(file):
    start_pc = base.read_unit16(file)
    line_number = base.read_int16(file)
    return LineNumberTableEntry(start_pc, line_number)


def read_local_variable_table(file, pool, name_index, length):
    entry_length = base.read_int16(file)
    line_number_table = [read_local_variable_table_entry(file)
                         for i in range(entry_length)]
    return LocalVariableTable(line_number_table)


def read_local_variable_table_entry(file):
    start_pc = base.read_unit16(file)
    line_number = base.read_int16(file)
    return LocalVariableTableEntry(start_pc, line_number)
