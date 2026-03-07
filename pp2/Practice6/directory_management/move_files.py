#1
import shutil

shutil.move("data.txt", "backup/data.txt")
print("Файл жылжытылды")


#2
import shutil

shutil.move("data.txt", "backup/new_data.txt")
print("Файл жаңа атпен жылжытылды")

#3
import os
import shutil

files = ["a.txt", "b.txt", "c.txt"]

for file in files:
    shutil.move(file, "backup/" + file)

print("Бірнеше файл жылжытылды")

#4
import os

os.rename("data.txt", "backup/data.txt")
print("Файл os.rename арқылы жылжытылды")

#5
from pathlib import Path

source = Path("data.txt")
source.rename(Path("backup") / "new_name.txt")

print("Файл pathlib арқылы жылжытылды")
