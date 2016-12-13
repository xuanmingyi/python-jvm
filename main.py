import jvm
from pprint import pprint


def main():
    with open('java/HelloWorld.class', "rb") as file:
        class_file = jvm.read(file)
        pprint(class_file)


if __name__ == '__main__':
    main()
