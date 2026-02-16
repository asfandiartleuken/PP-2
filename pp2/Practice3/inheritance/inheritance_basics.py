# 1) Basic inheritance
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()


# 2) Child class adds new method
class Animal:
    def eat(self):
        print("Eating food")

class Cat(Animal):
    def meow(self):
        print("Meow")

c = Cat()
c.eat()
c.meow()


# 3) Override parent method
class Animal:
    def speak(self):
        print("Animal sound")

class Bird(Animal):
    def speak(self):
        print("Chirp")

b = Bird()
b.speak()


# 4) Use parent constructor
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, grade):
        super().__init__(name)
        self.grade = grade

s = Student("Alice", "A")
print(s.name, s.grade)


# 5) Check inheritance
class Vehicle:
    pass

class Car(Vehicle):
    pass

print(issubclass(Car, Vehicle))
print(isinstance(Car(), Vehicle))