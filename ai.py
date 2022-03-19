from player import Player
import random
import pygame
from constants import *


class AI(Player):
    def __init__(self, playerNum):
        super().__init__(playerNum)
        self.blitzTimeDelay = 0
        self.placeTimeDelay = 0
        self.stackTimeDelay = 0
        self.blitzPlaceAttempt = False
        self.stackingPilePlaceAttempt = False
        self.placePilePlaceAttempt = False
        self.index = -1
        self.indexB = -1
        self.indices = (-1, -1)


    def blitzPilePlayAttempt(self, board, indexToPlace):
        #if there is no attempt to place, check for one
        if indexToPlace == -1:
            indexList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            random.shuffle(indexList)
            for x in indexList:
                if len(self.blitzPile) > 0 and self.playAttempt(board, x, self.blitzPile[0]):
                    # because the score cannot be incremented until card actually placed
                    self.score = self.score - 1
                    self.blitzTimeDelay = pygame.time.get_ticks()
                    return x
            return -1

        #if there was an attempt to place, and there has been a long enough time delay, and if the current play attempt is valid
        elif indexToPlace != -1 and pygame.time.get_ticks() > self.blitzTimeDelay + AI_WAIT_TIME:
                if self.playAttempt(board, indexToPlace, self.blitzPile[0]):
                    self.playResultForBlitzPile(True, board, indexToPlace)
                #if current play attempt was not valid
                else:
                    self.score = self.score - 1
                return -1

        #if there was an attempt to place but not enough time has passed
        return indexToPlace

    def placePilePlayAttempt(self, board, indexToPlace):
        # if there is no attempt to place, check for one
        if indexToPlace == -1:
            indexList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            random.shuffle(indexList)
            for x in indexList:
                if len(self.placePile) > 0 and self.playAttempt(board, x, self.placePile[0]):
                    # because the score cannot be incremented until card actually placed
                    self.score = self.score - 1
                    self.placeTimeDelay = pygame.time.get_ticks()
                    return x
            return -1

        # if there was an attempt to place, and there has been a long enough time delay, and if the current play attempt is valid
        elif indexToPlace != -1 and pygame.time.get_ticks() > self.placeTimeDelay + AI_WAIT_TIME:
            if self.playAttempt(board, indexToPlace, self.placePile[0]):
                self.playResultForPlacePile(True, board, indexToPlace)
            # if current play attempt was not valid
            else:
                self.score = self.score - 1
            return -1

        # if there was an attempt to place but not enough time has passed
        return indexToPlace

    def stackingPilesPlayAttempt(self, board, indexToPlace, stackPileIndex):
        # if there is no attempt to place, check for one
        if indexToPlace == -1:
            for q in range(0, 3):
                indexList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                random.shuffle(indexList)
                for x in indexList:
                    if len(self.stackingPiles[q]) > 0 and self.playAttempt(board, x, self.stackingPiles[q][0]):
                        # because the score cannot be incremented until card actually placed
                        self.score = self.score - 1
                        self.stackTimeDelay = pygame.time.get_ticks()
                        return x, q
                return -1, -1

        # if there was an attempt to place, and there has been a long enough time delay, and if the current play attempt is valid
        elif indexToPlace != -1 and pygame.time.get_ticks() > self.stackTimeDelay + AI_WAIT_TIME:
            if self.playAttempt(board, indexToPlace, self.stackingPiles[stackPileIndex][0]):
                self.playResultForStackPile(True, board, indexToPlace, stackPileIndex)
            # if current play attempt was not valid
            else:
                self.score = self.score - 1
            return -1, -1

        # if there was an attempt to place but not enough time has passed
        return indexToPlace, stackPileIndex



    def playCards(self, board):


        if self.blitzPlaceAttempt == False and self.stackingPilePlaceAttempt == False and self.placePilePlaceAttempt == False:
            self.index = self.blitzPilePlayAttempt(board, -1)
            if self.index != -1:
                self.blitzPlaceAttempt = True
        if self.blitzPlaceAttempt == False and self.stackingPilePlaceAttempt == False and self.placePilePlaceAttempt == False:
            self.indices = self.stackingPilesPlayAttempt(board, -1, -1)
            if self.indices != (-1, -1):
                self.stackingPilePlaceAttempt = True
        if self.blitzPlaceAttempt == False and self.stackingPilePlaceAttempt == False and self.placePilePlaceAttempt == False:
            self.indexB = self.placePilePlayAttempt(board, -1)
            if self.indexB != -1:
                self.placePilePlaceAttempt = True

        if self.blitzPlaceAttempt:
            if self.blitzPilePlayAttempt(board, self.index) == -1:
                self.index = -1
                self.blitzPlaceAttempt = False
        elif self.stackingPilePlaceAttempt:
            self.indices = self.stackingPilesPlayAttempt(board, self.indices[0], self.indices[1])
            if self.indices == (-1, -1):
                self.stackingPilePlaceAttempt = False
        elif self.placePilePlaceAttempt:
            self.indexB = self.placePilePlayAttempt(board, self.indexB)
            if self.indexB == -1:
                self.placePilePlaceAttempt = False




