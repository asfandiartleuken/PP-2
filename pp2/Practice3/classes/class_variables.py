# 1) Basic class variable
class Person:
    species = "Human"

p1 = Person()
p2 = Person()
print(p1.species, p2.species)


# 2) Shared value across objects
class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1

c1 = Counter()
c2 = Counter()
c3 = Counter()
print("Objects created:", Counter.count)


# 3) Modify class variable
class School:
    name = "ABC School"

School.name = "XYZ School"
print(School.name)


# 4) Access class variable via instance
class Car:
    wheels = 4

car = Car()
print(car.wheels)


# 5) Instance variable vs class variable
class Dog:
    species = "Canine"

    def __init__(self, name):
        self.name = name

d1 = Dog("Buddy")
d2 = Dog("Max")
print(d1.name, d1.species)
print(d2.name, d2.species)