class Student(object):
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def get_age(self):
        return self.__age


def function1():
    pass


x = lambda i: i

print(type(abs))
