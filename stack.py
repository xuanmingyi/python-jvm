from utils import panic


class Stack(object):
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.frames = []

    @property
    def size(self):
        return len(self.frames)

    def push(self, frame):
        if self.size >= self.maxSize:
            panic("java.lang.StackOverflowError")
        self.frames.append(frame)

    def pop(self):
        if self.size == 0:
            panic("jvm stack is empty")
        return self.frames.pop()

    def top(self):
        if self.size == 0:
            panic("jvm stack is empty")
        return self.frames[self.size - 1]
