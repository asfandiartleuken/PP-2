# 1) Basic continue in for loop
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

# 2) Skip even numbers
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)

# 3) Skip a specific value in list
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num == 4:
        continue
    print(num)

# 4) Continue with string characters
word = "python"
for char in word:
    if char == "h":
        continue
    print(char)

# 5) Skip numbers greater than 5
for i in range(1, 10):
    if i > 5:
        continue
    print(i)
