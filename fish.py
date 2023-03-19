import datetime
import math
import random
import time

import pygame

from FishData import FishData

SPRITEPATH = "./assets/images/sprites/"

class Fish(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, genesis="khor-pond", parent=None):
        super().__init__()
        self.fishData = FishData(genesis, parent)

        self.direction = "RIGHT"
        self.flip = 1
        self.sprites = []
        self.leftSprite = []
        self.rightSprite = []
        self.loadSprite(genesis)
        
        self.image = self.sprites[self.currentSprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.rect.left = pos_x
        self.rect.top = pos_y
        self.rect.right = pos_x + 100
        self.currentSprite = 0
        self.rect = self.image.get_rect()
        self.survivalTime = 0
        self.gaveBirth = False

    def getFishData(self):
        return self.fishData

    def getFishPosTL(self):
        return self.rect.topleft

    def getFishPosX(self):
        return self.rect.left

    def getFishPosY(self):
        return self.rect.top

    def die(self):
        self.kill()

    def flipSprite(self):
        if self.flip == 1:
            self.sprites = self.rightSprite
        elif self.face == -1:
            self.sprites = self.leftSprite

        self.currentSprite = 0

    def loadSprite(self, genesis):
        path = SPRITEPATH + "local-pond/" if genesis == "khor-pond" else SPRITEPATH + "foreign-pond/"

        self.loadSpriteLeft(path)
        self.loadSpriteRight(path, self.rightSprite)

    def loadSpriteLeft(self, path):
        for i in range(1, 5):
            spritePath = path + str(i) + ".png"
            img = pygame.image.load(str(spritePath))
            img = pygame.transform.scale(img, (100, 100))
            self.leftSprite.append(img)
        self.currentSprite = 0

    def loadSpriteRight(self, path, container):
        for i in range(1, 5):
            spritePath = path + str(i) + ".png"
            img = pygame.image.load(str(spritePath))
            img = pygame.transform.scale(img, (100, 100))
            img = pygame.transform.flip(img, True, False)
            container.apped(img)
        self.sprites = container.copy()
        self.currentSprite = 0

    def setStaytime(self, time):
        self.staytime = time

    def getStaytime(self):
        return str(self.staytime)

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
    
