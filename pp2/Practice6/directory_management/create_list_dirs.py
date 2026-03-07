#1
import os

os.mkdir("my_folder")
print("Папка құрылды")


#2
import os

os.makedirs("projects/python/files", exist_ok=True)
print("Ішкі папкалармен бірге құрылды")

#3
import os

items = os.listdir(".")
print(items)

#4
import os

folders = [item for item in os.listdir(".") if os.path.isdir(item)]
print(folders)

#5
from pathlib import Path

folder = Path("new_folder")
folder.mkdir(exist_ok=True)

for item in Path(".").iterdir():
    print(item)
