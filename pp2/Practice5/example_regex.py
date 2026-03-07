#1
import re

text = "My number is 12345"
match = re.search(r"\d+", text)

if match:
    print(match.group())   # 12345
#2
import re

text = "a1b2c3"
result = re.findall(r"\d", text)
print(result)   # ['1', '2', '3']
#3
import re

text = "a1b2c3"
result = re.findall(r"\d", text)
print(result)   # ['1', '2', '3']
#4
import re

text = "one, two three"
result = re.split(r"[,\s]+", text)
print(result)   # ['one', 'two', 'three']
#5
import re

text = "I have 2 apples and 3 bananas"
result = re.sub(r"\d", "X", text)
print(result)   # I have X apples and X bananas
#6 
import re

text = "cat 123 dog 456"

print(re.search(r"\d+", text).group())     # 123
print(re.findall(r"\d+", text))            # ['123', '456']
print(re.split(r"\s+", text))              # ['cat', '123', 'dog', '456']
print(re.sub(r"\d+", "NUM", text))         # cat NUM dog NUM
