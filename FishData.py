import random
import math
from datetime import datetime


def randId():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


def randCrowdTs():
    return random.randint(5, 20)


def randPheroTs():
    return random.randint(30, 60)


class FishData:
    def __init__(self, genesis, parentId=None):
        self.id = randId()
        self.state = "in-pond"
        self.status = "alive"
        self.genesis = genesis
        self.crowdTs = randCrowdTs()
        self.pheromone = 0
        self.pheromoneTs = randPheroTs()
        self.lifetime = 0
        self.staytime = 15
        self.parentId = parentId

        birth = datetime.now()
        self.birthtime = datetime.timestamp(birth)

    def getId(self):
        return self.id

    def getState(self):
        return self.state

    def getStatus(self):
        return self.status

    def getGenesis(self):
        return self.genesis

    def getCrowdThreshold(self):
        return self.crowdTs

    def getPheromone(self):
        return self.pheromone

    def getPheromoneThresh(self):
        return self.pheromoneTs

    def getLifetime(self):
        return self.lifetime

    def getStaytime(self):
        return self.staytime

    def getParentId(self):
        return self.parentId

    def setStatus(self, status):
        self.status = status

    def __str__(self):
        if self.parentId:
            return self.id + "Genesis:" + self.genesis + " Parent:" + self.parentId + " Lifetime: " + str(self.lifetime) + " Birthtime: " + str(self.birthtime)
        else:
            return self.id + "Genesis:" + self.genesis + " Lifetime: " + str(self.lifetime) + " Birthtime: " + str(self.birthtime)
