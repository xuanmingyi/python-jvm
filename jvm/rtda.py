class Thread(object):
    def __init__(self):
        self.stack = Stack(1024)

    def push_frame(self, frame):
        self.stack.push(frame)
        return self

    def pop_frame(self):
        return self.stack.pop()

    @property
    def current_frame(self):
        return self.stack.top


class Stack(object):
    def __init__(self, max_size):
        self.max_size = max_size
        self.data = []

    def __len__(self):
        return self.size

    def push(self, frame):
        if self.size < self.max_size:
            self.data.append(frame)
            return self
        else:
            raise Exception("Stack is full")

    def pop(self):
        if self.size > 0:
            return self.data.pop()
        else:
            raise Exception("Stack is empty")

    @property
    def top(self):
        return self.data[-1]

    @property
    def size(self):
        return len(self.data)


class Frame(object):
    def __init__(self, max_locals, max_stack):
        self.local_vars = LocalVars(max_locals)
        self.operand_stack = OperandStack(max_stack)


class Slot(object):
    pass


class LocalVars(object):
    def __init__(self, max_locals):
        self.max_locals = max_locals
        self.data = [0] * max_locals

    def set(self, index, value):
        self.data[index] = value

    def get(self, index):
        return self.data[index]

    def set_int(self, index, value):
        self.set(index, int(value))

    def get_int(self, index):
        return int(self.get(index))

    def set_float(self, index, value):
        self.set(index, float(value))

    def get_float(self, index):
        return float(self.get(index))

    def set_long(self, index, value):
        value = int(value)
        self.set(index, value)
        self.set(index + 1, value)

    def get_long(self, index):
        return self.get_int(index)

    def set_double(self, index, value):
        value = float(value)
        self.set(index, value)
        self.set(index + 1, value)

    def get_double(self, index):
        return self.get_float(index)

    def set_ref(self, index, value):
        self.set(index, value)

    def get_ref(self, index):
        return self.get(index)


class OperandStack(Stack):
    def push_int(self, value):
        return self.push(int(value))

    def pop_int(self):
        return int(self.pop())

    def push_float(self, value):
        return self.push(float(value))

    def pop_float(self):
        return float(self.pop())

    def push_long(self, value):
        self.push(int(value))
        return self.push(int(value))

    def pop_long(self):
        value = int(self.pop())
        self.pop()
        return value

    def push_double(self, value):
        self.push(float(value))
        return self.push(float(value))

    def pop_double(self):
        value = float(self.pop())
        self.pop()
        return value

    def push_ref(self, value):
        return self.push(value)

    def pop_ref(self):
        return self.pop()

    def push_slot(self, value):
        return self.push(value)

    def pop_slot(self):
        return self.pop()
