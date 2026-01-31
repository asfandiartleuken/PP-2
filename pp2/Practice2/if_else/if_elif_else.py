# 1) Basic if / elif / else example
x = 0
if x > 0:
    print("Positive number")
elif x < 0:
    print("Negative number")
else:
    print("Zero")

# 2) Grade evaluation
score = 82
if score >= 90:
    print("Grade: A")
elif score >= 75:
    print("Grade: B")
elif score >= 60:
    print("Grade: C")
else:
    print("Grade: F")

# 3) Age category check
age = 14
if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
else:
    print("Adult")

# 4) Day of the week check
day = 6
if day == 1:
    print("Monday")
elif day == 2:
    print("Tuesday")
elif day == 3:
    print("Wednesday")
elif day == 4:
    print("Thursday")
elif day == 5:
    print("Friday")
else:
    print("Weekend")

# 5) Login attempt check
attempts = 3
if attempts == 0:
    print("Account locked")
elif attempts <= 3:
    print("Attempts remaining")
else:
    print("Invalid attempt count")
