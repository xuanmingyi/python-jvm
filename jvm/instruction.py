from jvm.readers import base


class codeReader(object):
    def __init__(self, code):
        self.code = code
        self.pc = 0

    def read(self, size):
        end = self.pc + size
        if (end < len(self.code)):
            code = self.code[self.pc, end]
            self.pc = end
            return code
        else:
            raise Exception('No more code: {}'.format(self.code))


# const instuctions

def ACONST_NULL(frame, code):
    frame.operand_stack.push_ref(None)


def DCONST_0(frame, code):
    frame.operand_stack.push_double(0.0)


def DCONST_1(frame, code):
    frame.operand_stack.push_double(1.0)


def FCONST_0(frame, code):
    frame.operand_stack.push_float(0.0)


def FCONST_1(frame, code):
    frame.operand_stack.push_float(1.0)


def FCONST_2(frame, code):
    frame.operand_stack.push_float(2.0)


def ICONST_M1(frame, code):
    frame.operand_stack.push_int(-1)


def ICONST_0(frame, code):
    frame.operand_stack.push_int(0)


def ICONST_1(frame, code):
    frame.operand_stack.push_int(1)


def ICONST_2(frame, code):
    frame.operand_stack.push_int(2)


def ICONST_3(frame, code):
    frame.operand_stack.push_int(3)


def ICONST_4(frame, code):
    frame.operand_stack.push_int(4)


def ICONST_5(frame, code):
    frame.operand_stack.push_int(5)


def LCONST_0(frame, code):
    frame.operand_stack.push_long(0)


def LCONST_1(frame, code):
    frame.operand_stack.push_long(1)


# ipush instuctions

def BIPUSH(frame, code):
    value = base.read_int8(code)
    frame.operand_stack.push_int(value)


def SIPUSH(frame, code):
    value = base.read_int16(code)
    frame.operand_stack.push_int(value)


# load instuctions

def _iload(frame, index):
    value = frame.local_vars.get_int(index)
    frame.operand_stack.push_int(value)


def ILOAD(frame, code):
    index = base.read_int8(code)
    _iload(frame, index)


def ILOAD_0(frame, code):
    _iload(frame, 0)


def ILOAD_1(frame, code):
    _iload(frame, 1)


def ILOAD_2(frame, code):
    _iload(frame, 2)


def ILOAD_3(frame, code):
    _iload(frame, 3)


# store instuctions

def _lstore(frame, index):
    value = frame.operand_stack.pop_long()
    frame.local_vars.set_long(index, value)


def LSTORE(frame, code):
    index = base.read_int8(code)
    _lstore(frame, index)


def LSTORE_0(frame, code):
    _lstore(frame, 0)


def LSTORE_1(frame, code):
    _lstore(frame, 1)


def LSTORE_2(frame, code):
    _lstore(frame, 2)


def LSTORE_3(frame, code):
    _lstore(frame, 3)


# stack instuctions

def POP(frame, code):
    frame.operand_stack.pop_solt()


def POP_2(frame, code):
    frame.operand_stack.pop_solt()
    frame.operand_stack.pop_solt()


# dup instuctions

def DUP(frame, code):
    slot = frame.operand_stack.pop_solt()
    frame.operand_stack.push_solt(slot)
    frame.operand_stack.push_solt(slot)


def DUP_X1(frame, code):
    pass


def DUP_X2(frame, code):
    pass


def DUP_2(frame, code):
    pass


def DUP2_X1(frame, code):
    pass


def DUP2_X2(frame, code):
    pass
