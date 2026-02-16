# 1) Sort numbers in ascending order
numbers = [5, 2, 9, 1, 7]
sorted_numbers = sorted(numbers, key=lambda x: x)
print(sorted_numbers)

# 2) Sort numbers by absolute value
nums = [-10, 5, -3, 2, -1]
sorted_abs = sorted(nums, key=lambda x: abs(x))
print(sorted_abs)

# 3) Sort words by length
words = ["python", "is", "awesome", "code"]
sorted_words = sorted(words, key=lambda w: len(w))
print(sorted_words)

# 4) Sort list of tuples by second element
pairs = [(1, 3), (4, 1), (2, 2), (5, 0)]
sorted_pairs = sorted(pairs, key=lambda item: item[1])
print(sorted_pairs)

# 5) Sort list of dictionaries by age
people = [
    {"name": "Alice", "age": 22},
    {"name": "Bob", "age": 19},
    {"name": "Charlie", "age": 25}
]
sorted_people = sorted(people, key=lambda person: person["age"])
print(sorted_people)