import threading
from PondData import PondData
from fish import Fish
import random
from random import randint
from Client import Client

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

    def pheromoneCloud(self):
        pheromone = randint(2, 20)
        for fish in self.fishes:
            fish.increasePheromone(pheromone)
            print("inrease phero")

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
                self.pondData.fishes.remove(f)
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
                        self.migrateFish(index, destination)
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
        self.network = Client(self.pondData)
        # msg_handler = threading.Thread(target=self.network.get_msg)
        # msg_han6dler.start()
        # send_handler = threading.Thread(target=self.network.send_pond)
        # send_handler.start()
        # lifetime_handler = threading.Thread(
        #     target=self.network.handle_lifetime)
        # lifetime_handler.start()
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))

        bg = pygame.image.load("./assets/images/background/bg.jpg")
        bg = pygame.transform.scale(bg, (1280, 720))
        pygame.display.set_caption("Fish Haven Project")

        app = QApplication(sys.argv)
        clock = pygame.time.Clock()
        pregnant_time = pygame.time.get_ticks()
        update_time = pygame.time.get_ticks()
        other_pond_list = []

        self.addFish(Fish())
        running = True
        while running:
            if len(self.fishes) > 15:
                while (len(self.fishes) > 16):
                    kill = randint(0, len(self.fishes) - 1)
                    self.removeFish(self.fishes[kill])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.movingSprites.update()
            screen.blit(bg, [0, 0])
            self.movingSprites.draw(screen)

            other_pond_list = []
            # if len(self.network.messageQ) > 0:
            #     self.msg = self.network.messageQ.pop()
            #     if (self.msg.action == "MIGRATE"):
            #         newFish = Fish(50, randint(
            #             50, 650), self.msg.data['fish'].genesis, self.msg.data['fish'].parentId)
            #         print("ADD MIGRATED FISH")
            #         self.addFish(newFish)

            screen.fill((0, 0, 0))
            screen.blit(bg, [0, 0])

            for fish in self.movingSprites:
                screen.blit(fish.image, fish.rect)

            time_since_new_birth = pygame.time.get_ticks() - pregnant_time
            time_since_update = pygame.time.get_ticks() - update_time

            if time_since_update > 1000:
                self.update()
                update_time = pygame.time.get_ticks()

            if (time_since_new_birth > 5000):
                print("phero cloud deploy")
                self.pheromoneCloud()
                pregnant_time = pygame.time.get_ticks()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    p = Pond()
    p.run()
