from PondData import PondData
from Fish import Fish
from random import randint
import sys
import pygame
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtGui

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

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))

        bg = pygame.image.load("./assets/images/background/bg.jpg")
        bg = pygame.transform.scale(bg, (1280, 720))
        pygame.display.set_caption("Fish Haven Project")

        app = QApplication(sys.argv)
        other_pond_list = []

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.blit(bg, [0,0])
            pygame.display.flip()
        pygame.quit()