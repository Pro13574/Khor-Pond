import datetime
import math
import random
import time


class Fish:
    def __init__(self, pos_x, pos_y):
        self.id = self.randId()
        self.genesis = "genesis"
        # self.threshold = 10
        self.lifetime = 60
        self.status = "alive"
        self.staytime = 15
        self.sprites = []
        self.leftSprite = []
        self.rightSprite = []
        

    def setStaytime(self, time):
        self.staytime = time

    def getStaytime(self):
        return str(self.staytime)

    def randId(self):
        digits = [i for i in range(0, 10)]
        random_str= ""
        for i in range(6):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])
        return random_str

    def beImmortal(self):
        countdown(self.lifetime)
        self.status = "immortal"
        print(self.getInfo())

    def hatching(self):
        fry = Fish()
        randTime = random.randint(1, 15)
        self.setStaytime(randTime)
        fry.setStaytime(randTime)
        print(fry.getInfo())
        countdown(randTime)
        print("migrate")

    def migrate(self):
        if self.staytime == 0:
            print()

    def crowding(self):
        pass

    def getId(self):
        return self.id

    def getInfo(self):
        return "Fish:" + self.getId() + "\n" + "Genesis name: " + self.genesis + "\nStatus: " + self.status
        

def countdown(sec):
 
    while sec > 0:
        timer = datetime.timedelta(seconds = sec)
        print(timer, end="\r")
        time.sleep(1)
        sec -= 1
 
    return True

if __name__ == "__main__":
    fish = Fish()
    print(fish.getInfo())
    fish.hatching()
    fish.beImmortal()
    
