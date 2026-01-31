# 1) Basic break in for loop
for i in range(1, 10):
    if i == 5:
        break
    print(i)

# 2) Stop loop when value is found
numbers = [3, 6, 9, 12, 15]
for num in numbers:
    if num == 9:
        print("Target found")
        break
    print(num)

# 3) Break after first even number
for i in range(1, 10):
    if i % 2 == 0:
        print("First even number:", i)
        break

# 4) Password check using for loop
password = "admin"
for _ in range(3):
    user_input = input("Enter password: ")
    if user_input == password:
        print("Access granted")
        break
else:
    print("Access denied")

# 5) Break loop on negative number
numbers = [4, 7, 2, -1, 5]
for n in numbers:
    if n < 0:
        print("Negative number found")
        break
    print(n)
