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

    def update(self, speed):
        # if self.attack_animation == True:
        self.currentSprite += speed
        if int(self.currentSprite) >= len(self.sprites):
            self.currentSprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def move(self, speed_x):
        if self.rect.left <= 0:
            print("bump left wall")
            self.flip = 1
            print("x axis" + str(self.rect.left) + str(self.flip))
            self.flipSprite()

        elif self.rect.left >= 1180:
            print("bump right wall")
            self.flip = -1
            print("x axis" + str(self.rect.left) + str(self.flip))
            self.flipSprite()

        speed_x = random.randint(1, 5) * self.flip

        self.rect.x += speed_x
        self.update(0.05)

    def increasePheromone(self, n):
        self.fishData.pheromone += n

    def beImmortal(self):
        countdown(self.lifetime)
        self.fishData.setStatus("immortal")
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
        if self.fishData.getStaytime() == 0:
            print("The fish should migrate to another pond")

    def crowding(self):
        pass

    def getId(self):
        return self.fishData.getId()

    def getInfo(self):
        return "Fish:" + self.fishData.getId() + "\n" + "Genesis name: " + self.genesis + "\nStatus: " + self.fishData.status

    def isPregnant(self):
        return self.fishData.pheromone >= self.fishData.pheromoneTs

    def updateLifeTime(self):
        # self.in_pond_sec += 1
        self.fishData.lifetime -= 1
        if self.fishData.lifetime == 0:
            self.fishData.status = "dead"

    def resetPheromone(self):
        self.fishData.pheromone = 0

    def getGenesis(self):
        return self.fishData.getGenesis()

    def getCrowdThresh(self):
        return self.fishData.getCrowdThreshold()

    def giveBirth(self):
        self.gaveBirth = True


def countdown(sec):

    while sec > 0:
        timer = datetime.timedelta(seconds=sec)
        print(timer, end="\r")
        time.sleep(1)
        sec -= 1

    return True


if __name__ == "__main__":
    fish = Fish()
    print(fish.getInfo())
    fish.hatching()
    fish.beImmortal()
