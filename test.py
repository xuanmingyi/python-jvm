from class_file import Class

with open("java/Gauss.class", "rb") as f:
    rf = Class(f.read())
