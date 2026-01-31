# 1) Basic while loop
i = 1
while i <= 5:
    print(i)
    i += 1

# 2) Sum numbers using while loop
total = 0
num = 1
while num <= 5:
    total += num
    num += 1
print("Sum:", total)

# 3) Countdown using while loop
count = 5
while count > 0:
    print(count)
    count -= 1
print("Done")

# 4) User input loop
password = "1234"
user_input = ""
while user_input != password:
    user_input = input("Enter password: ")
print("Access granted")

# 5) Break while loop
i = 1
while True:
    if i == 4:
        break
    print(i)
    i += 1
