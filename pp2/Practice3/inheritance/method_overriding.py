# 1) Basic method overriding
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

d = Dog()
d.speak()


# 2) Override with different behavior
class Shape:
    def area(self):
        print("Undefined area")

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        print("Area:", self.w * self.h)

r = Rectangle(4, 5)
r.area()


# 3) Override but still call parent method
class Person:
    def introduce(self):
        print("I am a person")

class Student(Person):
    def introduce(self):
        super().introduce()
        print("I am also a student")

s = Student()
s.introduce()


# 4) Multiple child classes overriding same method
class Bird:
    def move(self):
        print("Bird moves")

class Sparrow(Bird):
    def move(self):
        print("Sparrow flies")

class Penguin(Bird):
    def move(self):
        print("Penguin swims")

Sparrow().move()
Penguin().move()


# 5) Polymorphism example
animals = [Dog(), Sparrow(), Penguin()]
for a in animals:
    a.move() if hasattr(a, "move") else a.speak()