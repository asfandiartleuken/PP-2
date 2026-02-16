# 1) Simple function without parameters
def greet():
    print("Hello, welcome!")

greet()

# 2) Function with parameters
def greet_user(name):
    print("Hello,", name)

greet_user("Alice")

# 3) Function returning a value
def add(a, b):
    return a + b

result = add(3, 5)
print("Sum:", result)

# 4) Function with default parameter
def power(base, exponent=2):
    return base ** exponent

print(power(4))
print(power(2, 3))

# 5) Function using conditional logic
def check_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

print(check_even(7))