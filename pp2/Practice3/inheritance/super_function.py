# 1) Call parent constructor with super()
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Alice", "A")
print(s.name, s.grade)


# 2) Extend parent method
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def speak(self):
        super().speak()
        print("Dog barks")

d = Dog()
d.speak()


# 3) Use super() in multiple inheritance chain
class A:
    def show(self):
        print("Class A")

class B(A):
    def show(self):
        super().show()
        print("Class B")

class C(B):
    def show(self):
        super().show()
        print("Class C")

c = C()
c.show()


# 4) Access parent attributes
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model

car = Car("Toyota", "Camry")
print(car.brand, car.model)


# 5) Modify behavior but keep parent logic
class Logger:
    def log(self):
        print("Base log")

class FileLogger(Logger):
    def log(self):
        super().log()
        print("Logging to file")

fl = FileLogger()
fl.log()