# 1) Basic instance method
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, my name is", self.name)

p = Person("Alice")
p.greet()


# 2) Method that modifies object state
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

c = Counter()
c.increment()
c.increment()
print("Counter:", c.value)


# 3) Method with parameters
class Calculator:
    def multiply(self, a, b):
        return a * b

calc = Calculator()
print("Result:", calc.multiply(3, 4))


# 4) Class method using @classmethod
class School:
    school_name = "ABC School"

    @classmethod
    def change_name(cls, new_name):
        cls.school_name = new_name

School.change_name("XYZ School")
print(School.school_name)


# 5) Static method using @staticmethod
class MathUtils:
    @staticmethod
    def is_even(num):
        return num % 2 == 0

print(MathUtils.is_even(6))