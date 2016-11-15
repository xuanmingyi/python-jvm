class Attribute(object):
    pass


class Code(Attribute):
    def __init__(self, *args, **kwargs):
        self.max_stack = kwargs.get("max_stack")
        self.max_locals = kwargs.get("max_locals")
        self.code_length = kwargs.get("code_length")
        self.code = kwargs.get("code")
