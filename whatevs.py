class Person:
    species = 'Homo sapiens'

    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age

    def greet(self, otherguy):
        print("Hello", otherguy, ". I'm", self.first_name, "and I'm", self.age)

    def get_info():
        print(Person.species)


robroy = Person('Rob Roy', 45)
anish = Person('Anish', 24)

robroy.greet('Anish')
anish.greet('RobRoy')

Person.get_info()


mystring = '{0} {1}'.format("thing", "thing")
print(mystring)


#Python anywhere
#DJANGO GIRLS  (tutorial on getting started with Python Anywhered)

# change the get functions to normal variable calls
# classes are camelCase

# mydict = {}
# mydict['key'] = value

# tweak the tubefocus iteration and variable referring to use a dictionary so the variables are explicitly called instead of returning separate variables

#  check out import collecitons

