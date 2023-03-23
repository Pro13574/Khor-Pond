from PondData import PondData
from fish import Fish
from random import randint
import sys
import pygame
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtGui


class Pond:
    def __init__(self):
        self.name = "khor-pond"
        self.fishes = []
        self.movingSprites = pygame.sprite.Group()
        self.pondData = PondData(self.name)
        self.msg = ""
        self.network = None

    def getPondData(self):
        return self.pondData

    def getPopulation(self):
        return len(self.fishes)

    def spawnFish(self, parentFish=None):
        fishes = Fish(self.name, parentFish.getId())
        self.fishes.append(fishes)
        self.movingSprites.add(fishes)

    def pheromoneCloud(self):
        pheromone = randint(2, 20)
        for fish in self.fishes:
            fish.increasePheromone(pheromone)

            if fish.isPregnant():
                newFish = fish.hatch()
                print("A fry has born")
                self.addFish(newFish)
                fish.resetPheromone()

    def migrateFish(self, fishIndex):
        # def migrateFish(self, fishIndex, destination):
        migrateFish = self.fishes[fishIndex]
        self.removeFish(migrateFish)
        # self.network.migrate_fish(migrateFish.fishData, destination)

    def addFish(self, newFish):
        self.fishes.append(newFish)
        self.pondData.addFish(newFish.fishData)
        self.movingSprites.add(newFish)
        # self.network.pond = self.pondData

    def removeFish(self, fish):
        self.fishes.remove(fish)
        for f in self.pondData.fishes:
            if f.id == fish.getId():
                self.pondData.fishes.remove(fish)
                break
        # self.movingSprites.remove(fish)
        # self.network.pond = self.pondData

    def update(self, injectPheromone=False):
        for index, fish in enumerate(self.fishes):
            fish.updateLifeTime()
            if fish.fishData.status == "dead":
                self.removeFish(fish)
                continue
            self.pondData.setFish(fish.fishData)

            if len(self.network.other_ponds.keys()) > 0:
                if fish.getGenesis() != self.name and fish.survivalTime >= 5 and not fish.gaveBirth:
                    newFish = Fish(fish.fishData.genesis, fish.fishData.id)

                if fish.getGenesjs() == self.name and fish.survivalTime <= 15:
                    if random.getrandbits(1):
                        destination = random.choice(
                            list(self.network.other_pondsd.keys()))
                        self.migrateFish(indedx, destination)
                        parent = None
                        if (fish.fishData.parentId):
                            parent = fish.fishData.parentId
                        for index2, fish2 in enumerate(self.fishes):
                            if parent and fish2.fishData.parentId == parent or fish2.fishData.parentId == fish.getId():
                                self.migrate(index2, destination)
                                break
                        continue
                else:
                    destination = random.choice(
                        list(self.network.other_ponds.key()))
                    if self.getPopulation() > fish.getCrowdThresh():
                        self.migrateFish(index, destination)
                        continue
            if (injectPheromone):
                self.pheromoneCloud()
            self.network.pond = self.pondData

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))

        bg = pygame.image.load("./assets/images/background/bg.jpg")
        bg = pygame.transform.scale(bg, (1280, 720))
        pygame.display.set_caption("Fish Haven Project")

        app = QApplication(sys.argv)
        other_pond_list = []

        fish = Fish(genesis="khor-pond")
        self.movingSprites.add(fish)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.movingSprites.update()
            screen.blit(bg, [0, 0])
            self.movingSprites.draw(screen)
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    p = Pond()
    p.run()
