# 1) Double each number using map
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

# 2) Convert strings to uppercase
words = ["python", "code", "map"]
upper_words = list(map(lambda w: w.upper(), words))
print(upper_words)

# 3) Add two lists element-wise
a = [1, 2, 3]
b = [4, 5, 6]
summed = list(map(lambda x, y: x + y, a, b))
print(summed)

# 4) Calculate squares
nums = [2, 4, 6, 8]
squares = list(map(lambda n: n ** 2, nums))
print(squares)

# 5) Extract lengths of words
text = ["apple", "banana", "kiwi"]
lengths = list(map(lambda word: len(word), text))
print(lengths)