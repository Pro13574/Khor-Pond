class PondData:
    def __init__(self, pondName):
        self.pondName = pondName
        self.fishes = []

    def __str__(self):
        fishId = ""
        for fish in self.fishes:
            fishId += fish.getId() + " "
            print(fish)
        return self.pondName + " " + str(len(self.fishes))
    
    def getPondName(self):
        return self.pondName
    
    def getPopulation(self):
        return len(self.fishes)

    def addFish(self, fishData):
        for i in range(len(self.fishes)):
            if self.fishes[i].id == fishData.id:
                return
        self.fishes.append(fishData)

    def getFishById(self, fishId):
        #res = None -> Dunno what this for
        # for fish in self.fishes:
        #     if fish.id == fishId:
        #         return fish
        for i in range(len(self.fishes)):
            if self.fishes[i].id == fishId:
                return self.fishes[i]
    
    def setFish(self, newFishData):
        for i in range(len(self.fishes)):
            if self.fishes[i].id == newFishData.id:
                self.fishes[i] = newFishData
                return

    def migrateFish(self, fishId):
        for i in range(len(self.fishes)):
            if self.fishes[i].id == fishId:
                self.fishes.pop(i)
                return