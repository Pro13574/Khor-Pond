from datetime import datetime
import math
import random
import time

import pygame

from FishData import FishData

from vivisystem.client import VivisystemClient
from vivisystem.models import EventType, VivisystemFish, VivisystemPond

SPRITEPATH = "./assets/images/sprites/"


def randId():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    return random_str


class Fish(pygame.sprite.Sprite):
    def __init__(self, genesis="khor-pond", parent=None, data: FishData = None):
        super().__init__()
        self.fishData = data or FishData(
            genesis, id=randId(), parentId=parent)
        self.direction = random.choice(["left", "right"])
        self.frame = 0
        self.sprites: dict[str, list[pygame.Surface]] = {
            "left": [],
            "right": []
        }
        # self.flip = 1
        # self.sprites = []
        # self.leftSprite = []
        # self.rightSprite = []

        self.currentSprite = 0
        self.loadSprite(genesis)
        # self.image = self.sprites[self.direction]
        # self.rect.topleft = [pos_x, pos_y]
        # self.rect.left = pos_x
        # self.rect.top = pos_y
        # self.rect.right = pos_x + 100
        # self.rect = self.image.get_rect()
        self.image = self.sprites[self.direction][self.frame]
        self.rect = self.image.get_rect()
        self.survivalTime = 0
        self.gaveBirth = False

        self.rect.x = random.randint(0, 1280 - self.rect.width)
        self.rect.y = random.randint(0, 720 - self.rect.height)

    @classmethod
    def from_vivisystemFish(cls, fish: VivisystemFish):
        return cls(data=FishData(genesis=fish.genesis, id=fish.fish_id, parentId=fish.parent_id, lifetime=fish.lifetime, pheromoneTs=fish.pheromone_threshold, crowdTs=fish.crowd_threshold))

    def to_vivisystemFish(self):
        return VivisystemFish(self.getId(), self.getParentId(), self.getGenesis(), self.getCrowdThresh(), self.getPheromoneThresh(), self.getLifetime())

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

    # def flipSprite(self):
    #     if self.flip == 1:
    #         self.sprites = self.rightSprite
    #     elif self.flip == -1:
    #         self.sprites = self.leftSprite

    #     self.currentSprite = 0

    # def loadSprite(self, genesis):
    #     path = SPRITEPATH + "local-pond/" if genesis == "khor-pond" else SPRITEPATH + "foreign-pond/"

    #     self.loadSpriteLeft(path)
    #     self.loadSpriteRight(path, self.rightSprite)
    #     self.loadSpriteRight(path, self.sprites)
    #     self.loadSpriteLeft(path)
    #     self.loadSpriteRight(path, self.rightSprite)

    # def loadSpriteLeft(self, path):
    #     for i in range(1, 5):
    #         spritePath = path + str(i) + ".png"
    #         img = pygame.image.load(str(spritePath))
    #         img = pygame.transform.scale(img, (100, 100))
    #         self.leftSprite.append(img)
    #     self.currentSprite = 0

    # def loadSpriteRight(self, path, container):
    #     for i in range(1, 5):
    #         spritePath = path + str(i) + ".png"
    #         img = pygame.image.load(str(spritePath))
    #         img = pygame.transform.scale(img, (100, 100))
    #         img = pygame.transform.flip(img, True, False)
    #         #container.apped(img)
    #     self.sprites = container.copy()
    #     self.currentSprite = 0

    def loadSprite(self, genesis: str):
        path = "./assets/images/sprites/"
        if genesis == "khor-pond":
            path += "local-pond/"
        else:
            path += "foreign-pond/"

        for i in range(1, 5):
            image_path = f"{path}/{i}.png"
            image = pygame.image.load(image_path).convert_alpha()
            image_left = pygame.transform.scale(image, (100, 100))
            image_right = pygame.transform.flip(image_left, True, False)
            self.sprites["left"].append(image_left)
            self.sprites["right"].append(image_right)

        self.frame = 0

    def update(self, speed=1):
        # if self.attack_animation == True:
        # self.currentSprite += speed
        # if int(self.currentSprite) >= len(self.sprites):
        #     self.currentSprite = 0
        # self.image = self.sprites[int(self.current_sprite)]
        self.frame = (self.frame + 0.1) % len(self.sprites[self.direction])
        self.image = self.sprites[self.direction][int(self.frame)]
        if self.direction == "left":
            self.rect.x -= speed
            if self.rect.x <= 0:
                self.direction = "right"
        else:
            self.rect.x += speed
            if self.rect.x >= 1280 - self.rect.width:
                self.direction = "left"

    # def move(self, speed_x):
    #     if self.rect.left <= 0:
    #         print("bump left wall")
    #         self.flip = 1
    #         print("x axis" + str(self.rect.left) + str(self.flip))
    #         self.flipSprite()

    #     elif self.rect.left >= 1180:
    #         print("bump right wall")
    #         self.flip = -1
    #         print("x axis" + str(self.rect.left) + str(self.flip))
    #         self.flipSprite()

    #     speed_x = random.randint(1, 5) * self.flip

    #     self.rect.x += speed_x
    #     self.update(0.05)

    def increasePheromone(self, n):
        self.fishData.pheromone += n
        print("phero now: ", self.fishData.pheromone)

    def beImmortal(self):
        countdown(self.lifetime)
        self.fishData.setStatus("immortal")
        print(self.getInfo())

    def hatch(self):
        fry = Fish(self.fishData.getGenesis(), self.fishData.getId())

        # randTime = random.randint(1, 15)
        # self.fishData.setStaytime(randTime)
        # fry.fishData.setStaytime(randTime)
        # print(fry.getInfo())
        # countdown(randTime)
        # print("migrate")
        return fry

    def migrate(self):
        if self.fishData.getStaytime() == 0:
            print("The fish should migrate to another pond")

    def crowding(self):
        pass

    def getInfo(self):
        return "Fish:" + self.fishData.getId() + "\n" + "Genesis name: " + self.genesis + "\nStatus: " + self.fishData.status

    def isPregnant(self):
        return self.fishData.pheromone >= self.fishData.pheromoneTs

    def updateLifeTime(self):
        # self.in_pond_sec += 1
        now = datetime.now()
        time = datetime.timestamp(now)
        self.fishData.lifetime = 60 - int(time - self.fishData.birthtime)
        if self.fishData.lifetime <= 0:
            print(self.fishData.getId() + "dead")
            self.fishData.status = "dead"
        # if (time - self.fishData.birthtime) > 10:
        #     print(str(self.fishData.getId) + "dead")
        #     self.fishData.status = "dead"

    def resetPheromone(self):
        self.fishData.pheromone = 0

    def getGenesis(self):
        return self.fishData.getGenesis()

    def getId(self):
        return self.fishData.getId()

    def getParentId(self):
        return self.fishData.getParentId()

    def getLifetime(self):
        return self.fishData.getLifetime()

    def getPheromoneThresh(self):
        return self.fishData.getPheromoneThresh()

    def getCrowdThresh(self):
        return self.fishData.getCrowdThresh()

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
