from enum import Enum


class Name(Enum):
    Code = "Code"
    ConstantValue = "ConstantValue"
    Deprecated = "Deprecated"
    Exceptions = "Exceptions"
    LineNumberTable = "LineNumberTable"
    LocalVariableTable = "LocalVariableTable"
    SourceFile = "SourceFile"
    Synthetic = "Synthetic"
    Unparsed = "Unparsed"


class Attribute(object):
    def __init__(self, pool, name_index, length):
        self.name_index = name_index
        self.length = length

    @property
    def name(self):
        return self.pool.get_utf8(self.name_index).value


class Unparsed(Attribute):
    def __init__(self, pool, name_index, length, info):
        super().__init__(pool, name_index, length)
        self.info = info


class Deprecated(Attribute):
    pass


class Synthetic(Attribute):
    pass


class SourceFile(Attribute):
    def __init__(self, pool, name_index, length, source_file_index):
        super().__init__(pool, name_index, length)
        self.source_file_index = source_file_index

    @property
    def file_name(self):
        return self.pool.get_utf8(self.source_file_index).value


class ConstantValue(Attribute):
    def __init__(self, pool, name_index, length, constant_value_index):
        super().__init__(pool, name_index, length)
        self.constant_value_index = constant_value_index


class Code(Attribute):
    def __init__(self, pool, name_index, length,
                 max_stack, max_locals, code_length, code,
                 exception_tables, attributes):
        super().__init__(pool, name_index, length)
        self.max_stack = max_stack
        self.max_locals = max_locals
        self.code_length = code_length
        self.code = code
        self.exception_tables = exception_tables
        self.exception_table_length = len(exception_tables)
        self.attributes = attributes
        self.attribute_count = len(attributes)


class ExceptionTable(object):
    def __init__(self, start_pc, end_pc, handler_pc, catch_type):
        self.start_pc = start_pc
        self.end_pc = end_pc
        self.handler_pc = handler_pc
        self.catch_type = catch_type


class Exception(Attribute):
    def __init__(self, pool, name_index, length, exception_index_table):
        super().__init__(pool, name_index, length)
        self.exception_index_table = exception_index_table
        self.number_of_exceptions = len(exception_index_table)


class LineNumberTable(Attribute):
    def __init__(self, pool, name_index, length, line_number_table):
        super().__init__(pool, name_index, length)
        self.line_number_table = line_number_table


class LineNumberTableEntry(object):
    def __init__(self, start_pc, line_number):
        self.start_pc = start_pc
        self.line_number = line_number


class LocalVariableTable(Attribute):
    def __init__(self, pool, name_index, length, local_variable_table):
        super().__init__(pool, name_index, length)
        self.local_variable_table = local_variable_table


class LocalVariableTableEntry(object):
    def __init__(self, start_pc, line_number):
        self.start_pc = start_pc
        self.line_number = line_number
