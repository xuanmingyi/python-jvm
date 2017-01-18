from jvm.readers import base
from . import logic


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


# swap instuctions

def SWAP(frame, code):
    slot1 = frame.operand_stack.pop_solt()
    slot2 = frame.operand_stack.pop_solt()
    frame.operand_stack.push_solt(slot1)
    frame.operand_stack.push_solt(slot2)


# math instuctions

def ADD(frame, code):
    value1 = frame.operand_stack.pop_int()
    value2 = frame.operand_stack.pop_int()
    result = value1 + value2
    frame.operand_stack.push_int(result)


def SUB(frame, code):
    value1 = frame.operand_stack.pop_int()
    value2 = frame.operand_stack.pop_int()
    result = value1 - value2
    frame.operand_stack.push_int(result)


def MUL(frame, code):
    value1 = frame.operand_stack.pop_int()
    value2 = frame.operand_stack.pop_int()
    result = value1 * value2
    frame.operand_stack.push_int(result)


def DIV(frame, code):
    value1 = frame.operand_stack.pop_int()
    value2 = frame.operand_stack.pop_int()
    if value2 == 0:
        raise Exception("ArithmeticException by zore")
    else:
        result = value1 - value2
        frame.operand_stack.push_int(result)


def NEG(frame, code):
    value = frame.operand_stack.pop_int()
    result = -value
    frame.operand_stack.push_int(result)


def IREM(frame, code):
    value1 = frame.operand_stack.pop_int()
    value2 = frame.operand_stack.pop_int()
    if value2 == 0:
        raise Exception("ArithmeticException by zore")
    else:
        result = value1 % value2
        frame.operand_stack.push_int(result)


def DREM(frame, code):
    value1 = frame.operand_stack.pop_double()
    value2 = frame.operand_stack.pop_double()
    if value2 == 0:
        raise Exception("ArithmeticException by zore")
    else:
        result = value1 % value2
        frame.operand_stack.pop_double(result)


# sh instuctions

def ISHL(frame, code):
    offset = frame.operand_stack.pop_int()
    value = frame.operand_stack.pop_int()
    offset = offset & 0x1f
    result = value << offset
    frame.operand_stack.push_int(result)


def ISHR(frame, code):
    offset = frame.operand_stack.pop_int()
    value = frame.operand_stack.pop_int()
    offset = offset & 0x1f
    result = value >> offset
    frame.operand_stack.push_int(result)


def IUSHR(frame, code):
    offset = frame.operand_stack.pop_int()
    value = frame.operand_stack.pop_int()
    offset = offset & 0x1f
    result = value >> offset
    frame.operand_stack.push_int(result)


def LSHL(frame, code):
    offset = frame.operand_stack.pop_int()
    value = frame.operand_stack.pop_int()
    offset = offset & 0x3f
    result = value << offset
    frame.operand_stack.push_int(result)


def LSHR(frame, code):
    offset = frame.operand_stack.pop_int()
    value = frame.operand_stack.pop_int()
    offset = offset & 0x3f
    result = value >> offset
    frame.operand_stack.push_int(result)


def LUSHR(frame, code):
    offset = frame.operand_stack.pop_int()
    value = frame.operand_stack.pop_int()
    offset = offset & 0x3f
    result = value >> offset
    frame.operand_stack.push_int(result)


# and instuctions

def IAND(frame, code):
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    result = value1 & value2
    frame.operand_stack.push_int(result)


def LAND(frame, code):
    value2 = frame.operand_stack.pop_long()
    value1 = frame.operand_stack.pop_long()
    result = value1 & value2
    frame.operand_stack.push_long(result)


def IOR(frame, code):
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    result = value1 | value2
    frame.operand_stack.push_int(result)


def LOR(frame, code):
    value2 = frame.operand_stack.pop_long()
    value1 = frame.operand_stack.pop_long()
    result = value1 | value2
    frame.operand_stack.push_long(result)


def IXOR(frame, code):
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    result = value1 ^ value2
    frame.operand_stack.push_int(result)


def LXOR(frame, code):
    value2 = frame.operand_stack.pop_long()
    value1 = frame.operand_stack.pop_long()
    result = value1 ^ value2
    frame.operand_stack.push_long(result)


# iinc instuctions

def IINC(frame, code):
    index = base.read_int8(code)
    const = base.read_interger8(code)
    value = frame.local_vars.get_int(index)
    value += const
    frame.local_vars.set_int(index, value)


# d2x instuctions

def D2F(frame, code):
    value = frame.operand_stack.pop_double()
    result = float(value)
    frame.operand_stack.push_float(result)


def D2I(frame, code):
    value = frame.operand_stack.pop_double()
    result = int(value)
    frame.operand_stack.push_int(result)


def D2L(frame, code):
    value = frame.operand_stack.pop_double()
    result = int(value)
    frame.operand_stack.push_long(result)


# lcmp instuctions

def LCMP(frame, code):
    value2 = frame.operand_stack.pop_long()
    value1 = frame.operand_stack.pop_long()
    if value1 > value2:
        frame.operand_stack.push_int(1)
    elif value1 == value2:
        frame.operand_stack.push_int(0)
    else:
        frame.operand_stack.push_int(-1)


# fcmp<op> and dcmp<op> instuctions
######### for the following 4
######### what should NaN be

def FCMPG(frame, code):
    value2 = frame.operand_stack.pop_float()
    value1 = frame.operand_stack.pop_float()
    if value1 > value2:
        frame.operand_stack.push_int(1)
    elif value1 == value2:
        frame.operand_stack.push_int(0)
    elif value1 < value2:
        frame.operand_stack.push_int(-1)
    else:
        frame.operand_stack.push_int(1)


def FCMPL(frame, code):
    value2 = frame.operand_stack.pop_float()
    value1 = frame.operand_stack.pop_float()
    if value1 > value2:
        frame.operand_stack.push_int(1)
    elif value1 == value2:
        frame.operand_stack.push_int(0)
    elif value1 < value2:
        frame.operand_stack.push_int(-1)
    else:
        frame.operand_stack.push_int(-1)


def DCMPG(frame, code):
    value2 = frame.operand_stack.pop_double()
    value1 = frame.operand_stack.pop_double()
    if value1 > value2:
        frame.operand_stack.push_int(1)
    elif value1 == value2:
        frame.operand_stack.push_int(0)
    elif value1 < value2:
        frame.operand_stack.push_int(-1)
    else:
        frame.operand_stack.push_int(1)


def DCMPL(frame, code):
    value2 = frame.operand_stack.pop_double()
    value1 = frame.operand_stack.pop_double()
    if value1 > value2:
        frame.operand_stack.push_int(1)
    elif value1 == value2:
        frame.operand_stack.push_int(0)
    elif value1 < value2:
        frame.operand_stack.push_int(-1)
    else:
        frame.operand_stack.push_int(-1)


# if<cond> instuctions

def IFEQ(frame, code):
    offset = base.read_int8(code)
    value = frame.operand_stack.pop_int()
    if value == 0:
        logic.branch(frame, offset)


def IFNE(frame, code):
    offset = base.read_int8(code)
    value = frame.operand_stack.pop_int()
    if value != 0:
        logic.branch(frame, offset)


def IFLT(frame, code):
    offset = base.read_int8(code)
    value = frame.operand_stack.pop_int()
    if value < 0:
        logic.branch(frame, offset)


def IFLE(frame, code):
    offset = base.read_int8(code)
    value = frame.operand_stack.pop_int()
    if value <= 0:
        logic.branch(frame, offset)


def IFGT(frame, code):
    offset = base.read_int8(code)
    value = frame.operand_stack.pop_int()
    if value > 0:
        logic.branch(frame, offset)


def IFGE(frame, code):
    offset = base.read_int8(code)
    value = frame.operand_stack.pop_int()
    if value >= 0:
        logic.branch(frame, offset)


# if_imcp<cond> instuctions

def IF_ICMPEQ(frame, code):
    offset = base.read_int8(code)
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    if value1 == value2:
        logic.branch(frame, offset)


def IF_ICMPNE(frame, code):
    offset = base.read_int8(code)
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    if value1 != value2:
        logic.branch(frame, offset)


def IF_ICMPLT(frame, code):
    offset = base.read_int8(code)
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    if value1 < value2:
        logic.branch(frame, offset)


def IF_ICMPLE(frame, code):
    offset = base.read_int8(code)
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    if value1 <= value2:
        logic.branch(frame, offset)


def IF_ICMPGT(frame, code):
    offset = base.read_int8(code)
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    if value1 > value2:
        logic.branch(frame, offset)


def IF_ICMPGE(frame, code):
    offset = base.read_int8(code)
    value2 = frame.operand_stack.pop_int()
    value1 = frame.operand_stack.pop_int()
    if value1 >= value2:
        logic.branch(frame, offset)


# if_amcp<cond> instuctions

def IF_ACMPEQ(frame, code):
    offset = base.read_int8(code)
    ref2 = frame.operand_stack.pop_ref()
    ref1 = frame.operand_stack.pop_ref()
    if ref1 == ref2:
        logic.branch(frame, offset)


def IF_ACMPNE(frame, code):
    offset = base.read_int8(code)
    ref2 = frame.operand_stack.pop_ref()
    ref1 = frame.operand_stack.pop_ref()
    if ref1 != ref2:
        logic.branch(frame, offset)


# goto instuction

def GOTO(frame, code):
    offset = base.read_int8(code)
    logic.branch(frame, offset)
