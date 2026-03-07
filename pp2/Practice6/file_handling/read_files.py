#1
file = open("data.txt", "r", encoding="utf-8")
content = file.read()
print(content)
file.close()
#2
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

#3
with open("data.txt", "r", encoding="utf-8") as file:
    line = file.readline()
    print(line)

#4
with open("data.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    print(lines)

#5
with open("data.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
