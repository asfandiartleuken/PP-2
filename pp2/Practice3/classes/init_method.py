# 1) Basic __init__ method
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Alice")
print(p.name)


# 2) Multiple attributes
class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

s = Student("Bob", 17, "A")
print(s.name, s.age, s.grade)


# 3) Default value in __init__
class Car:
    def __init__(self, brand, color="Black"):
        self.brand = brand
        self.color = color

c1 = Car("Toyota")
c2 = Car("BMW", "Red")
print(c1.brand, c1.color)
print(c2.brand, c2.color)


# 4) Using __init__ with calculation
class Rectangle:
    def __init__(self, width, height):
        self.area = width * height

r = Rectangle(4, 5)
print("Area:", r.area)


# 5) Boolean attribute in __init__
class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.is_active = balance > 0

acc = Account("Alice", 100)
print(acc.owner, acc.is_active)