# 1) Using *args to accept multiple numbers
def sum_all(*args):
    total = 0
    for num in args:
        total += num
    print("Sum:", total)

sum_all(1, 2, 3, 4)

# 2) Using **kwargs to accept key-value data
def show_profile(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

show_profile(name="Alice", age=20, city="Astana")

# 3) Combine normal argument and *args
def multiply(factor, *numbers):
    for n in numbers:
        print(n * factor)

multiply(2, 3, 4, 5)

# 4) Combine normal argument and **kwargs
def greet_user(greeting, **info):
    print(greeting)
    for key, value in info.items():
        print(key, ":", value)

greet_user("Hello", name="Bob", country="Kazakhstan")

# 5) Using both *args and **kwargs
def full_info(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

full_info(1, 2, 3, name="Alice", role="student")