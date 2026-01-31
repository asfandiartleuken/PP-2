# 1) Basic break example
i = 1
while i <= 10:
    if i == 5:
        break
    print(i)
    i += 1

# 2) Stop loop when condition is met
number = 0
while True:
    number += 1
    if number == 3:
        break
    print(number)

# 3) Search for a value using break
numbers = [2, 4, 6, 8, 10]
target = 6
i = 0
while i < len(numbers):
    if numbers[i] == target:
        print("Target found")
        break
    i += 1

# 4) Password check with break
password = "admin"
while True:
    user_input = input("Enter password: ")
    if user_input == password:
        print("Correct password")
        break
    print("Wrong password")

# 5) Break loop after first even number
i = 1
while i <= 10:
    if i % 2 == 0:
        print("First even number:", i)
        break
    i += 1
