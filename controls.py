import pygame
from constants import *

class Controls():
    #checks if mouse is in the area of a certain object
    def mouseInArea(self, mouseCoords, topLeftCoord, objSize):
        if mouseCoords[0] >= topLeftCoord[0] and \
                mouseCoords[0] <= topLeftCoord[0] + objSize[0] and \
                mouseCoords[1] >= topLeftCoord[1] and \
                mouseCoords[1] <= topLeftCoord[1] + objSize[1]:
            return True
        return False

    #checks is mouse is hovering over a valid card (parameter is an array of coordinates rather than one coordinate)
    def hoveringOverCard(self, mouseCoords, playerCoords):
        for i in range(len(playerCoords)):
            if self.mouseInArea(mouseCoords, playerCoords[i], (CARD_SIZE_X, CARD_SIZE_Y)):
                return i
        return -1

    def leftButtonClick(self):
        return pygame.mouse.get_pressed(3)[0]

    def rightButtonClick(self):
        return pygame.mouse.get_pressed(3)[2]

    def getMousePos(self):
        return pygame.mouse.get_pos()

