# 1) Basic for loop
for i in range(1, 6):
    print(i)

# 2) Loop through a list
numbers = [10, 20, 30, 40]
for num in numbers:
    print(num)

# 3) Sum numbers using for loop
total = 0
for i in range(1, 6):
    total += i
print("Sum:", total)

# 4) Loop with index using range
names = ["Alice", "Bob", "Charlie"]
for i in range(len(names)):
    print(i, names[i])

# 5) String iteration
word = "Python"
for char in word:
    print(char)
