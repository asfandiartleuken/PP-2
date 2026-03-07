#1
import shutil

shutil.copy("data.txt", "data_copy.txt")
print("Файл көшірілді")

#2
import shutil

shutil.copyfile("data.txt", "backup.txt")
print("Файл copyfile арқылы көшірілді")

#3
import os

os.remove("data.txt")
print("Файл өшірілді")

#4
import os

if os.path.isfile("data.txt"):
    os.remove("data.txt")
    print("Файл өшірілді")
else:
    print("Файл табылмады")

#5
import shutil
import os

shutil.copy("data.txt", "archive_data.txt")
os.remove("data.txt")

print("Файл көшірілді және бастапқы файл өшірілді")
