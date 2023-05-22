import random
import matplotlib.pyplot as plt

# Constants

SIMULATION_TIME_YEARS = 400

startPopulation = 50
infantMortality = 5
youthMortality = 45
agricultureUnitPeople = 1.55
disasterChance = 0.116
fertilityx = 18
fertilityy = 45
food = 10
peopleDictionary = []


class Person:
    def __init__(self, age):
        self.gender = random.randint(0,1)
        self.age = age
        self.pregnant = 0


class PopulationSimulation:
     
    @property
    def population(self):
        return len(self.peoples)

    def __init__(self, _peoples: Person,
                 _startPopilation,
                 _infantMortality, _youthMortality,
                 _agricultureUnitPeople,
                 _disasterChance,
                 _fertilityx, _fertilityy, 
                 _food):
        
        self.peoples=_peoples
        self.startPopilation=_startPopilation
        self.infantMortality=_infantMortality
        self.youthMortality=_youthMortality
        self.agricultureUnitPeople=_agricultureUnitPeople
        self.disasterChance=_disasterChance
        self.fertilityx=_fertilityx
        self.fertilityy=_fertilityy
        self.food=_food

        # statistics
        self.counter = 0

        self.foodReserve = {}
        self.oldAgeDeath = {}
        self.disasterHistory = {}
        self.newborns = {}

    def tick(self):
        self.counter += 1

    def harvest(self):

        ablePeople = 0  # люди, которые способны работать на поле
        for person in self.peoples:
            if person.age > 8:
                ablePeople +=1

        self.food += ablePeople * self.agricultureUnitPeople

        if self.food < len(self.peoples):
            sizeBefore = len(self.peoples)

            self.peoples = self.peoples[ : self.food]    # ?
            self.food = 0

            self.foodReserve[self.counter] = -(sizeBefore - len(self.peoples))
        else:
            self.food -= len(self.peoples)
            self.foodReserve[self.counter] = self.food


    def selection(self):
        counterDeath = 0

        for people in self.peoples:

            people.age += 1

            if (people.age > 80):
                self.peoples.remove(people)
                counterDeath += 1

        self.oldAgeDeath[self.counter] = counterDeath

    def disaster(self):
        if (random.randint(0, 100) < self.disasterChance * 100):
            sizeBefore = len(self.peoples)

            self.peoples = self.peoples[0 : int(len(self.peoples) * (1 - self.disasterChance))]

            self.disasterHistory[self.counter] = sizeBefore - len(self.peoples)

    def reproduce(self):
        sizeBefore = len(self.peoples)

        for person in self.peoples:
            if person.gender == 1:
                if person.age > self.fertilityx:
                    if person.age < self.fertilityy:
                        if random.randint(0, 100) < 25:  # шанс родить 25%
                            if random.randint(0, 100) > self.infantMortality:
                                self.peoples.append(Person(0))

        self.newborns[self.counter] = len(self.peoples) - sizeBefore


# ------------ main code ------------

peoples = [ Person(random.randint(18, 60)) for i in range(startPopulation) ]

simulation = PopulationSimulation(peoples, 
                           startPopulation, 
                           infantMortality, youthMortality, 
                           agricultureUnitPeople, 
                           disasterChance, 
                           fertilityx, fertilityy, 
                           food)

nowYear = 0
dataX = []
dataY = []

plt.figure()
plt.subplot(141)
plt.title("Population (peoples / year)")

counterDataUpdate = 20  # update data every this counter years

while (nowYear < SIMULATION_TIME_YEARS and
       simulation.population > 1 and
       simulation.population < 10000):

    nowYear += 1
    simulation.tick()

    simulation.harvest()

    simulation.selection()

    simulation.disaster()

    simulation.reproduce()

    simulation.infantMortality *= 0.98
    
    print("----------------")
    print(f"foodReserve -> {simulation.foodReserve[nowYear]}") if nowYear in simulation.foodReserve else ...
    print(f"oldAgeDeath -> {simulation.oldAgeDeath[nowYear]}") if nowYear in simulation.oldAgeDeath else ...
    print(f"disasterHistory -> {simulation.disasterHistory[nowYear]}") if nowYear in simulation.disasterHistory else ...
    print(f"newborns -> {simulation.newborns[nowYear]}") if nowYear in simulation.newborns else ...

    
    print(f"{nowYear} -> {simulation.population}")
    print("----------------")

    dataX += [nowYear]
    dataY += [simulation.population]

    plt.scatter(nowYear, simulation.population)
    if nowYear % counterDataUpdate == 0:
        plt.pause(0.001)


# print("-------------- Statistics --------------")

plt.subplot(142)
plt.title("Population (peoples / year)")
plt.plot(dataX, dataY)

# show disasterHistory statistics

disasterY = []
for i in dataX:
    if (i in simulation.disasterHistory):
        disasterY += [simulation.disasterHistory[i]]
    else:
        disasterY += [0]

plt.subplot(143)
plt.title("Disasters (peoples / year)")
plt.plot(dataX, disasterY)

# show newborns statistics

newbornsY = []
for i in dataX:
    if (i in simulation.newborns):
        newbornsY += [simulation.newborns[i]]
    else:
        newbornsY += [0]

plt.subplot(144)
plt.title("Newborns (peoples / year)")
plt.plot(dataX, newbornsY)

plt.show()

print("Program finished!")