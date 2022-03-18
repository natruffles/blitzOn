import pygame
import os
from constants import *
from gameBoard import GameBoard
from player import Player
from ai import AI
from setupScreen import SetupScreen
from time import sleep
import random
from controls import Controls


numofcards = 1000
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlitzOn!")

startScreen = SetupScreen()
controls = Controls()

clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
    mousePos = controls.getMousePos()
    buttonClicked = controls.leftButtonClick()
    startScreen.hoveringOrClickingButtons(screen, mousePos, buttonClicked)
    clock.tick(60)






