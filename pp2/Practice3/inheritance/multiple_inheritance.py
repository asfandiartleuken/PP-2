# 1) Basic multiple inheritance
class Father:
    def skill1(self):
        print("Driving")

class Mother:
    def skill2(self):
        print("Cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skill1()
c.skill2()


# 2) Child class uses methods from both parents
class Writer:
    def write(self):
        print("Writing a story")

class Artist:
    def draw(self):
        print("Drawing a picture")

class Creator(Writer, Artist):
    pass

cr = Creator()
cr.write()
cr.draw()


# 3) Constructor from both parents
class A:
    def __init__(self):
        print("A initialized")

class B:
    def __init__(self):
        print("B initialized")

class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)

c = C()


# 4) Method resolution order (MRO)
class X:
    def show(self):
        print("From X")

class Y:
    def show(self):
        print("From Y")

class Z(X, Y):
    pass

z = Z()
z.show()


# 5) Override method in child
class Engine:
    def start(self):
        print("Engine starts")

class Electric:
    def start(self):
        print("Electric power on")

class HybridCar(Engine, Electric):
    def start(self):
        print("Hybrid system ready")

h = HybridCar()
h.start()