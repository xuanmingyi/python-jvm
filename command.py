#import argparse
#
#
#class Command(object):
#    def __init__(self, argv):
#        self.parser = argparse.ArgumentParser(description="python jvm.")
#
#        self.parser.add_argument("classname", help="class name")
#        self.parser.add_argument("-cp", "--classpath", default="",
#            dest="classpath")
#
#        self.parser.add_argument("-v", "--version", default=False,
#            action="store_true", help="print version and exit.")
#
#        self.args = self.parser.parse_args(argv)
#
#        self.classname = self.args.classname
#        self.version = self.args.version
#        self.classpath = self.args.classpath
