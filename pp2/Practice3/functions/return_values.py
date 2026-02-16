# 1) Return a single value
def square(number):
    return number * number

result = square(4)
print("Square:", result)

# 2) Return multiple values
def get_user():
    name = "Alice"
    age = 20
    return name, age

user_name, user_age = get_user()
print(user_name, user_age)

# 3) Return boolean value
def is_even(num):
    return num % 2 == 0

print(is_even(6))
print(is_even(7))

# 4) Return string based on condition
def check_pass(score):
    if score >= 50:
        return "Passed"
    return "Failed"

print(check_pass(75))
print(check_pass(40))

# 5) Use returned value in calculation
def add(a, b):
    return a + b

total = add(5, 10) * 2
print("Result:", total)