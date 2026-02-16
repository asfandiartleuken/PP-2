# 1) Basic class definition
class Person:
    name = "Unknown"

p1 = Person()
print(p1.name)


# 2) Class with __init__ constructor
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = Student("Alice", 20)
print(s1.name, s1.age)


# 3) Class method
class Car:
    def __init__(self, brand):
        self.brand = brand

    def show_brand(self):
        print("Brand:", self.brand)

c1 = Car("Toyota")
c1.show_brand()


# 4) Modify object attribute
class Book:
    def __init__(self, title):
        self.title = title

b1 = Book("Python Basics")
b1.title = "Advanced Python"
print(b1.title)


# 5) Multiple objects
class Animal:
    def __init__(self, species):
        self.species = species

a1 = Animal("Cat")
a2 = Animal("Dog")
print(a1.species, a2.species)