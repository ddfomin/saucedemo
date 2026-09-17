class Animal:
    def __init__(self, age=None):
        self.name = 1
        self.age = age
        self.x = 10

    def __str__(self):
        return f"{self.name}, {self.age} ==== {self.__dict__}"

dog = Animal("jack")
print(dog)
print()

class Dog(Animal):
    def __init__(self, age, new):
        super().__init__(age)
        self.new = new

    def __str__(self):
        return f"{self.name}, {self.age}, {self.new} ==== {self.__dict__}"

d = Dog( 10, "new")
print(d)


