import pygame
import os
from constants import *
from gameBoard import GameBoard
from player import Player
from ai import AI
from setupScreen import SetupScreen
from time import sleep
import random


numofcards = 1000
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlitzOn!")

CardImage = pygame.image.load(os.path.join('images/cards', 'blue_5.png'))
CardImage = pygame.transform.rotate(CardImage, 90)
screen.blit(CardImage, (0,0))
pygame.display.update()
sleep(60)

startScreen = SetupScreen(SCREEN_WIDTH, SCREEN_HEIGHT, "title_screen.png", "title_screen.png","title_screen.png","title_screen.png","title_screen.png","title_screen.png")
startScreen.displayTitleScreenBG(screen, numofcards, 0.2, 1)
sleep(60)
