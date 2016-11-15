import abc
import sys
import os.path
import zipfile
import struct

from struct import Struct

from utils import panic


class Entry(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, path):
        self.path = os.path.abspath(path)

    @abc.abstractmethod
    def readClass(self, className):
        raise NotImplementedError


class DirEntry(Entry):

    def readClass(self, className):
        fileName = os.path.join(self.path, className)
        with open(fileName, "rb") as f:
            data = f.read()
        return data

class ZipEntry(Entry):

    def readClass(self, className):
        with zipfile.ZipFile(self.path, "r") as f:
            if className in f.namelist():
                data = f.read(className)
            else:
                raise
        return data

def build(path):
    if ( path.lower().endswith(".jar") or path.lower().endswith(".zip") ):
        return ZipEntry(path)
    return DirEntry(path)

class CONSTANT_Utf8(object):
    def __init__(self, string):
        self.string = string

class CONSTANT_Class(object):
    def __init__(self, nameIndex):
        self.nameIndex = nameIndex

class CONSTANT_String(object):
    def __init__(self, stringIndex):
        self.stringIndex = stringIndex

class CONSTANT_Fieldref(object):
    def __init__(self, classIndex, nameAndTypeIndex):
        self.classIndex = classIndex
        self.nameAndTypeIndex = nameAndTypeIndex

class CONSTANT_Methodref(object):
    def __init__(self, classIndex, nameAndTypeIndex):
        self.classIndex = classIndex
        self.nameAndTypeIndex = nameAndTypeIndex

class CONSTANT_NameAndType(object):
    def __init__(self, nameIndex, descriptorIndex):
        self.nameIndex = nameIndex
        self.descriptorIndex = descriptorIndex

class ClassFile(object):

    def __init__(self, data):
        self.maps = [
            self.CONSTANT_Undefined,                #                               0
            self.CONSTANT_Utf8,                     # CONSTANT_Utf8                 1
            self.CONSTANT_Undefined,                # 
            self.CONSTANT_Integer,                  # CONSTANT_Integer              3
            self.CONSTANT_Float,                    # CONSTANT_Float                4
            self.CONSTANT_Long,                     # CONSTANT_Long                 5
            self.CONSTANT_Double,                   # CONSTANT_Double               6
            self.CONSTANT_Class,                    # CONSTANT_Class                7
            self.CONSTANT_String,                   # CONSTANT_String               8
            self.CONSTANT_Fieldref,                 # CONSTANT_Fieldref             9
            self.CONSTANT_Methodref,                # CONSTANT_Methodref            a
            self.CONSTANT_InterfaceMethodref,       # CONSTANT_InterfaceMethodref   b
            self.CONSTANT_NameAndType,              # CONSTANT_NameAndType          c
        ]


        self.CONSTANT = []
        self.data = data
        self.size = 0

        self.magic = self.read_u4()
        self.minorVersion = self.read_u2()
        self.majorVersion = self.read_u2()

        try:
            self.check_vaild()
        except:
            painc("invaild class file")


        self.constantPoolCount = self.read_u2()

        for i in range(1, self.constantPoolCount):
            tag = self.read_u1()
            if tag < len(self.maps):
                self.maps[tag]()
            print tag

        accessFlags = self.read_u2()
        print "0x%x"%accessFlags

        
        thisClass = self.read_u2()
        superClass = self.read_u2()

        print thisClass, superClass

        
        interfacesCount = self.read_u2()

        print interfacesCount


        # FIXME interfaces 
        # for i in interfacesCount

        # FIXME fields
        # fileds 

        fieldsCount = self.read_u2()

        print fieldsCount
        for i in range(fieldsCount):
            pass

        # methods

        methodsCount = self.read_u2()
        print methodsCount

        for i in range(methodsCount):
            accessFlags = self.read_u2()
            nameIndex = self.read_u2()
            descriptorIndex = self.read_u2()
            attributes_count = self.read_u2()
            print "accessFlags: %d %d %d %d"%(accessFlags, nameIndex, descriptorIndex, attributes_count)
            for i in range(attributes_count):
                attributeNameIndex = self.read_u2()
                attributeLength = self.read_u4()
                self._read(">{0}s".format(attributeLength))
                print "attr%d: name %d length %d "%(i, attributeNameIndex, attributeLength)

        # attributes 
        print self.read_u2()
        attributeNameIndex = self.read_u2()
        attributeLength = self.read_u4()
        self._read(">{0}s".format(attributeLength))

        print self.size == len(data)


    def CONSTANT_Utf8(self):
        length = self.read_u2()
        data = self._read(">{0}s".format(length))
        self.CONSTANT.append(CONSTANT_Utf8(data.encode("utf8")))

    def CONSTANT_Undefined(self):
        raise Exception()

    def CONSTANT_Integer(self):
        pass

    def CONSTANT_Float(self):
        pass

    def CONSTANT_Long(self):
        pass

    def CONSTANT_Double(self):
        pass

    def CONSTANT_Class(self):
        nameIndex = self.read_u2()
        self.CONSTANT.append(CONSTANT_Class(nameIndex))

    def CONSTANT_String(self):
        stringIndex = self.read_u2()
        self.CONSTANT.append(CONSTANT_String(stringIndex))

    def CONSTANT_Fieldref(self):
        classIndex = self.read_u2()
        nameAndTypeIndex = self.read_u2()
        self.CONSTANT.append(CONSTANT_Fieldref(classIndex, nameAndTypeIndex))

    def CONSTANT_Methodref(self):
        classIndex = self.read_u2()
        nameAndTypeIndex = self.read_u2()
        self.CONSTANT.append(CONSTANT_Methodref(classIndex, nameAndTypeIndex))

    def CONSTANT_InterfaceMethodref(self):
        pass

    def CONSTANT_NameAndType(self):
        nameIndex = self.read_u2()
        descriptorIndex = self.read_u2()
        self.CONSTANT.append(CONSTANT_NameAndType(nameIndex, descriptorIndex))

    def check_vaild(self):
        if self.magic != 0xcafebabe:
            raise
        if not self.check_version():
            raise

    def check_version(self):
        if self.majorVersion == 45:
            return True
        if self.majorVersion in [46, 47, 48, 49, 50, 51, 52] and  self.minorVersion == 0:
            return True
        return False

    def _read(self, _s):
        s = struct.Struct(_s)
        (data, ) = s.unpack(self.data[self.size:self.size+s.size])
        self.size += s.size
        return data

    def read_u1(self):
        return self._read(">B")

    def read_u2(self):
        return self._read(">H")

    def read_u4(self):
        return self._read(">I")

data = build(".").readClass("HelloWorld.class")
ClassFile(data)

