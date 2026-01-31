# 1) Basic continue example
i = 0
while i < 5:
    i += 1
    if i == 3:
        continue
    print(i)

# 2) Skip even numbers
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue
    print(num)

# 3) Skip specific value
count = 0
while count < 6:
    count += 1
    if count == 4:
        continue
    print(count)

# 4) Continue with user input
while True:
    user_input = input("Enter a number (0 to stop): ")
    if user_input == "0":
        break
    if int(user_input) < 0:
        continue
    print("You entered:", user_input)

# 5) Skip numbers greater than 5
i = 0
while i < 10:
    i += 1
    if i > 5:
        continue
    print(i)
