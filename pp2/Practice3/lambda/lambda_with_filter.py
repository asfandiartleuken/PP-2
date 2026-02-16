# 1) Filter even numbers
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)

# 2) Filter positive numbers
nums = [-3, -1, 0, 2, 4, -5]
positives = list(filter(lambda n: n > 0, nums))
print(positives)

# 3) Filter long words
words = ["cat", "elephant", "dog", "giraffe"]
long_words = list(filter(lambda w: len(w) > 3, words))
print(long_words)

# 4) Filter non-empty strings
texts = ["hello", "", "world", "", "python"]
non_empty = list(filter(lambda t: t != "", texts))
print(non_empty)

# 5) Filter numbers greater than 10
values = [5, 12, 7, 20, 3, 15]
greater_than_10 = list(filter(lambda v: v > 10, values))
print(greater_than_10)