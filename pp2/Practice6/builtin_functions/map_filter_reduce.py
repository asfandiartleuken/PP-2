#1
numbers = [1, 2, 3, 4, 5]

result = list(map(lambda x: x ** 2, numbers))
print(result)

#2
numbers = [1, 2, 3, 4, 5, 6]

result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)

#3
from functools import reduce

numbers = [1, 2, 3, 4, 5]

result = reduce(lambda x, y: x + y, numbers)
print(result)

#4
words = ["python", "code", "file"]

result = list(map(str.upper, words))
print(result)

#5
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

even_numbers = filter(lambda x: x % 2 == 0, numbers)
squares = map(lambda x: x ** 2, even_numbers)
result = reduce(lambda x, y: x + y, squares)

print(result)
