#1
def squares(n):
    for i in range(1, n + 1):
        yield i * i
N = int(input("Enter N: "))
for i in squares(N):
    print(i)
#2
def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input())
d = True
for i in even_numbers(n):

    if not d:
        print(",",end="")
    print(i,end="")
    d = False
#3
def generate_divisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

numbers = generate_divisible(int(input("number:")))

for num in numbers:
    print(num)
#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

a = int(input("Enter a: "))
b = int(input("Enter b: "))

for value in squares(a, b):
    print(value)
#5
def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input())

for num in countdown(n):
    print(num)    
