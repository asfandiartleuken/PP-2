#1
with open("data.txt", "w", encoding="utf-8") as file:
    file.write("Сәлем, Python!")

#2
with open("data.txt", "w", encoding="utf-8") as file:
    file.write("Бірінші жол\n")
    file.write("Екінші жол\n")
    file.write("Үшінші жол\n")

#3
lines = ["Алма\n", "Алмұрт\n", "Шие\n"]

with open("data.txt", "w", encoding="utf-8") as file:
    file.writelines(lines)

#4
with open("data.txt", "a", encoding="utf-8") as file:
    file.write("\nЖаңа ақпарат қосылды.")

#5
text = input("Мәтін енгіз: ")

with open("data.txt", "w", encoding="utf-8") as file:
    file.write(text)
