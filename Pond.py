import threading
from Dashboard import Dashboard
from FishData import FishData
from PondData import PondData
from Fish import Fish
from FishStore import FishStore
import random
from random import randint

import sys
import pygame
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtGui

from vivisystem.client import VivisystemClient
from vivisystem.models import EventType, VivisystemFish, VivisystemPond

UPDATE_EVENT = pygame.USEREVENT + 1
PHEROMONE_EVENT = pygame.USEREVENT + 2
NOTICE_DATABASE_EVENT = pygame.USEREVENT + 3


class Pond:
    def __init__(self, name: str, fishStore: FishStore, client: VivisystemClient = None):
        self.name: str = name
        self.fishStore: FishStore = fishStore
        self.fishes = []
        self.connectedPonds = {}
        self.movingSprites = pygame.sprite.Group()
        self.pondData = PondData(self.name)
        self.msg = ""
        self.client = client

    def getPondData(self):
        return self.pondData

    def getPopulation(self):
        return len(self.fishes)

    def handle_migrate(self, vivi_fish: VivisystemFish):
        fish = Fish.from_vivisystemFish(vivi_fish)
        self.add_fish(fish)
        print(f"Migrated fish {fish.get_id()} from {vivi_fish.genesis}")

    def handle_status(self, vivi_pond: VivisystemPond):
        self.connectedPonds[vivi_pond.name] = vivi_pond

    def handle_disconnect(self, pond_name: str):
        if pond_name in self.connectedPonds:
            del self.connectedPonds[pond_name]  # let's see if it works
            print(f"{pond_name} disconnected")

    def terminate(self):
        if self.client:
            self.client.disconnect()
        sys.exit()

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
        self.fishStore.add_fish(newFish.getFishData())
        # print(newFish.getFishData())
        # self.network.pond = self.pondData

    def removeFish(self, fish):
        self.fishes.remove(fish)
        for f in self.pondData.fishes:
            if f.id == fish.getId():
                self.pondData.fishes.remove(f)
                self.fishStore.remove_fish(f.id)
                break
        self.movingSprites.remove(fish)

        # self.network.pond = self.pondData

    def load_fishes(self):
        for fish in self.fishStore.get_fishes().values():
            self.addFish(fish)

    def update(self, injectPheromone=False):
        for index, fish in enumerate(self.fishes):
            fish.updateLifeTime()
            if fish.fishData.status == "dead":
                self.removeFish(fish)
                continue
            self.pondData.setFish(fish.fishData)

            if self.connectedPonds:
                if fish.getGenesis() != self.name and fish.survivalTime >= 5 and not fish.gaveBirth:
                    newFish = Fish(fish.fishData.genesis, fish.fishData.id)

                if fish.getGenesis() == self.name and fish.survivalTime <= 15:
                    pass
                elif fish.getGenesis() == self.name and fish.survivalTime >= 15:
                    destination = random.choice(list(self.connectedPonds))
                    self.client.migrate_fish(
                        destination, fish.toVivisystemFish())
                    self.removeFish(fish)
                else:
                    if self.getPopulation() > fish.getCrowdThresh():
                        destination = random.choice(list(self.connectedPonds))
                        self.client.migrate_fish(
                            destination, fish.toVivisystemFish())
                        self.removeFish(fish)
            if (injectPheromone):
                self.pheromoneCloud()
            # self.network.pond = self.pondData

    def run(self):
        # self.network = Client(self.pondData)
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
        self.load_fishes()
        self.addFish(Fish(parent=None))

        pygame.time.set_timer(UPDATE_EVENT, 1000)
        pygame.time.set_timer(NOTICE_DATABASE_EVENT, 1000)
        pygame.time.set_timer(PHEROMONE_EVENT, 2000)

        if self.client:
            handler_map = {
                EventType.MIGRATE: self.handle_migrate,
                EventType.STATUS: self.handle_status,
                EventType.DISCONNECT: self.handle_disconnect
            }
            for event_type, handler in handler_map.items():
                self.client.handle_event(event_type, handler)

        running = True
        while running:
            print("len fishes ", len(self.fishes))
            if len(self.fishes) > 15:
                while (len(self.fishes) > 16):
                    # print("looping")
                    kill = randint(0, len(self.fishes) - 1)
                    print(self.fishes[kill].getFishData())
                    self.removeFish(self.fishes[kill])

            for event in pygame.event.get():
                if event.type == UPDATE_EVENT:
                    self.update()
                if event.type == PHEROMONE_EVENT:
                    self.pheromoneCloud()
                if event.type == NOTICE_DATABASE_EVENT:
                    self.client.send_status(VivisystemPond(
                        self.name,
                        len(self.fishes),
                        1))
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        # TODO----------------------------------------EDIT PLEASE--------------------------------------
                        # print(self.fishes[0].getId())
                        allPondsNum = len(self.fishes)
                        for p in self.connectedPonds:
                            allPondsNum += p.total_fishes
                        dashboard = Dashboard(self, allPondsNum)
                    if event.key == pygame.K_LEFT:
                        viviDashboard = ViviDashboard(self.connectedPonds)
            # pond_handler = threading.Thread(target=app.exec_)
            # pond_handler.start()
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

                update_time = pygame.time.get_ticks()

            if (time_since_new_birth > 2000):
                # print("phero cloud inject")

                pregnant_time = pygame.time.get_ticks()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        self.terminate()

# if __name__ == "__main__":
#     p = Pond()
#     p.run()
