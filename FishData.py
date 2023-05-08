import random
import math
from datetime import datetime


def randCrowdTs():
    return random.randint(5, 20)


def randPheroTs():
    return random.randint(30, 60)


class FishData:
    def __init__(self, genesis: str, id: str, parentId: str = None, lifetime: int = None, pheromoneTs: int = None, crowdTs: int = None):
        self.id = id
        self.state = "in-pond"
        self.status = "alive"
        self.genesis = genesis
        self.crowdTs = crowdTs or randCrowdTs()
        self.pheromone = 0
        self.pheromoneTs = pheromoneTs or randPheroTs()
        self.lifetime = lifetime or 60
        self.staytime = 15
        self.parentId = parentId

        # print(self)
        # print("add-on", self.crowdTs, self.pheromoneTs)

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

    def getCrowdThresh(self):
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
            return str(self.id) + "Genesis:" + str(self.genesis) + " Parent:" + str(self.parentId) + " Lifetime: " + str(self.lifetime) + " Birthtime: " + str(self.birthtime) + "c " + str(self.crowdTs) + "p " + str(self.pheromoneTs)
        else:
            return self.id + "Genesis:" + self.genesis + " Lifetime: " + str(self.lifetime) + " Birthtime: " + str(self.birthtime)
