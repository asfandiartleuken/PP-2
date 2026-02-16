# 1) Simple lambda function
square = lambda x: x * x
print(square(5))

# 2) Lambda with two arguments
add = lambda a, b: a + b
print(add(3, 7))

# 3) Lambda inside print
print((lambda x: x * 2)(10))

# 4) Using lambda in condition
is_even = lambda n: n % 2 == 0
print(is_even(8))
print(is_even(5))

# 5) Lambda with if-else expression
check = lambda x: "Positive" if x > 0 else "Negative or Zero"
print(check(4))
print(check(-2))