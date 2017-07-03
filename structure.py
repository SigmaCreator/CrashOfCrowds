import re

class Auxin:
	def __init__(self, x, y, name):
		self.x = x
		self.y = y
		self.name = name
		self.minDistance = 200
		self.agent = None
		self.taken = False
		#self.cell = None
	def reset(self):
		self.minDistance = 200
		self.agent = None
		self.taken = False

class Cell:
	def __init__(self, x, y, name):
		self.x = x
		self.y = y
		self.name = name
		self.auxins = []
		self.people = []
	def add_auxin(self, auxin):
		self.auxins.append(auxin)
	def reset(self):
		self.people = []

class Person:
    personCount = 0

    def __init__(self, path):
        self.path = path
        Person.personCount += 1
	self.cell = None

    def addPos(self, position):
        self.path.append(position)

    def toString(self):
        sb = []
        for p in self.path:
            sb.append(p)
        return sb

    def getFirstPos(self):
        return self.path[0]

    def getLastPos(self):
        return self.path[len(self.path)-1]

class Frame:
    frameCount = 0

    def __init__(self, id):
        self.id = id
        self.people = []
        Frame.frameCount += 1

    def append(self, personID, position):
        idSet = set([p[0] for p in self.people])

        if personID not in idSet:
            self.people.append((personID, position))
            #print("Adicionou pessoa", personID, "no frame", self.id)

    def fetch(self):
        return self.people

people = []

frames = []

ratio = 0

threshold = 0

def printPeople():
    count = 0
    for p in people:
        print("Pessoa", count, ":", p.toString())
        count += 1

def printFrames():
    for frame in frames:
        print("Frame:", frame.id)
        print("People:", frame.fetch())

def readFile(path):

    with open(path) as file:
        data = file.readlines()
        ratio = float(data[0].replace("[","").replace("]",""))
        threshold = 1/ratio

        for line in data[1:len(data)-1]:

            path = []

            person = Person(path)

            content = line.rsplit()

            numberOfSteps = int(content[0])

            aux = re.findall(r'(\([0-9]+,[0-9]+,[0-9]+\))?', content[1])

            for pos in aux:
                if pos != "":
                    m = re.findall(r'([0-9]+)', pos)
                    x = float(m[0])*100/ratio
                    y = float(m[1])*100/ratio
                    t = int(m[2])

                    person.addPos((x,y,t))

                    newFrame = True

                    for frame in frames:
                        if frame.id == t:
                            frame.append(len(people),(x,y))
                            newFrame = False


                    if newFrame:
                        shinFureimu = Frame(t)
                        shinFureimu.append(len(people),(x,y))
                        frames.append(shinFureimu)

            people.append(person)

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
