# 1) Қарапайым if
x = 10
if x > 5:
    print("x 5-тен үлкен")

# 2) if / else
age = 16
if age >= 18:
    print("Рұқсат етілген")
else:
    print("Рұқсат етілмеген")

# 3) if / elif / else
score = 75
if score >= 90:
    print("A")
elif score >= 70:
    print("B")
else:
    print("C")

# 4) Boolean шартпен if
is_student = True
if is_student:
    print("Студент")
else:
    print("Студент емес")

# 5) Күрделі шарт (and)
age = 19
has_id = True
if age >= 18 and has_id:
    print("Кіруге болады")
else:
    print("Кіруге болмайды")
