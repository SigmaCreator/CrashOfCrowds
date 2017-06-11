import re

class Person:
    personCount = 0

    def __init__(self, path):
        self.path = path
        Person.personCount += 1

    def addPos(self, position):
        self.path.append(position)

    def toString(self):
        sb = []
        for p in self.path:
            sb.append(p)
        print(sb)

    def getFirstPos(self):
        return self.path[0]

    def getLastPos(self):
        return self.path[len(self.path)-1]

people = []

ratio = 0

threshold = 0

def printPeople():
    count = 0
    for p in people:
        print("Pessoa", count, ": ", p.toString())
        count += 1

def readFile():

    with open("Paths_D.txt") as file:
        data = file.readlines()
        ratio = float(data[0].replace("[","").replace("]",""))
        threshold = 1/ratio

        for line in data[1:len(data)-1]:
            path = []

            content = line.rsplit()

            numberOfSteps = int(content[0])

            aux = re.findall(r'(\([0-9]+,[0-9]+,[0-9]+\))?', content[1])

            for pos in aux:
                if pos != "":
                    m = re.findall(r'([0-9]+)', pos)
                    x = float(m[0])/ratio
                    y = float(m[1])/ratio
                    t = int(m[2])

                    path.append((x,y,t))

            print(path)
            person = Person(path)

            people.append(person)

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

readFile()

# printPeople()
