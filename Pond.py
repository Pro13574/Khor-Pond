from PondData import PondData
from random import randint

class Pond:
    def __init__(self):
        self.name = "khor-pond"
        self.fishes = []
        self.pondData = PondData(self.name)
        self.msg = ""
        self.network = None
    
    def getPopulation(self):
        return len(self.fishes)

    def spawnFish(self, parentFish = None):
        #declare tempFish here
        #self.fishes.append(tempFish)
        return 
    
    def migrateFish(self, fishIndex, destination):
        migrateFish = self.fishes[fishIndex]
        self.removeFish(migrateFish)
        #self.network.migrate_fish(migrateFish.fishData, destination)

    def addFish(self, newFishData):
        self.fishes.append(newFishData)
        #self.pondData.addFish(newFishData.fishData) fishData -> depends on our variable name
        #self.network.pond = self.pondData

    def removeFish(self, fish):
        self.fishes.remove(fish)
        for fish in self.pondData.fishes:
            if fish.id == fish.getId():
                self.pondData.fishes.remove(fish)
                break
        #self.network.pond = self.pondData

    def pheromoneCloud(self):
        pheromone = randint(2, 20)
        for fish in self.fishes:
            fish.increasePheromone(pheromone)
            if fish.isPregnant():
                newFish = Fish()
                self.addFish(newFish)
                self.pondData.addFish(newFish.fishData)
                fish.resetPheromone()
