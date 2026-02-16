# 1) Positional arguments
def introduce(name, age):
    print("Name:", name)
    print("Age:", age)

introduce("Alice", 20)

# 2) Keyword arguments
def describe_pet(animal, name):
    print("Animal:", animal)
    print("Name:", name)

describe_pet(name="Milo", animal="Cat")

# 3) Default arguments
def greet(name="Guest"):
    print("Hello,", name)

greet()
greet("Bob")

# 4) Variable number of arguments (*args)
def sum_numbers(*numbers):
    total = 0
    for n in numbers:
        total += n
    print("Sum:", total)

sum_numbers(1, 2, 3, 4)

# 5) Keyword variable arguments (**kwargs)
def show_info(**info):
    for key, value in info.items():
        print(key, ":", value)

show_info(name="Alice", age=21, city="Astana")