from constants import *
from card import Card
import pygame
import os
import random

class SetupScreen():
    def __init__(self, screenWidth, screenHeight, titleFile, playButtonFile, tutorialButtonFile, optionsButtonFile,
                 creditsButtonFile, exitButtonFile):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.titleImage = pygame.image.load(os.path.join('images', titleFile))
        self.playButtonImage = pygame.image.load(os.path.join('images', playButtonFile))
        self.tutorialButtonImage = pygame.image.load(os.path.join('images', tutorialButtonFile))
        self.optionsButtonImage = pygame.image.load(os.path.join('images', optionsButtonFile))
        self.creditsButtonImage = pygame.image.load(os.path.join('images', creditsButtonFile))
        self.exitButtonImage = pygame.image.load(os.path.join('images', exitButtonFile))

    #displays the background of the title screen
    def displayTitleScreenBG(self, screen, numberOfCards, lowerSizeMultiplier, upperSizeMultiplier):
        for i in range(numberOfCards):
            sizeMultiplier = random.uniform(lowerSizeMultiplier, upperSizeMultiplier)
            randomCardColor = random.choice(["red", "blue", "green", "yellow"])
            randomCardNumber = str(random.randrange(1, 10))
            randomCardFileName = randomCardColor + "_" + randomCardNumber + ".png"
            randomCardImage = pygame.image.load(os.path.join('images/cards', randomCardFileName))
            randomCardImage = pygame.transform.scale(randomCardImage, (randomCardImage.get_width() * sizeMultiplier, randomCardImage.get_height() * sizeMultiplier))
            xCoord = random.randint(-randomCardImage.get_width()-100, SCREEN_WIDTH+100)
            yCoord = random.randint(-randomCardImage.get_height()-100, SCREEN_HEIGHT+100)
            cardSurf = pygame.transform.rotate(randomCardImage, random.randint(0,359))
            screen.blit(cardSurf, (xCoord, yCoord))
            pygame.display.update()




    #displays all of the buttons in the title screen
    def displayTitleScreenButtons(self, screen):
        pass

