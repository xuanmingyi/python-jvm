from enum import Enum


class Flags(Enum):
    Public = 0x0001         # class field method
    Private = 0x0002        #       field method
    Protected = 0x0004      #       field method
    Static = 0x0008         #       field method
    Final = 0x0010          # class field method
    Super = 0x0020          # class
    Synchronized = 0x0020   #             method
    Volatile = 0x0040       #       field
    Bridge = 0x0040         #             method
    Transient = 0x0080      #       field
    Varargs = 0x0080        #             method
    Native = 0x0100         #             method
    Interface = 0x0200      # class
    Abstract = 0x0400       # class       method
    Strict = 0x0800         #             method
    Synthetic = 0x1000      # class field method
    Annotation = 0x2000     # class
    Enum = 0x4000           # class field
