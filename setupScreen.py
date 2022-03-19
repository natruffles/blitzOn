from constants import *
import pygame
import os
import random
from controls import Controls

class SetupScreen(Controls):
    def __init__(self):
        self.titleImage = pygame.image.load(os.path.join(TITLE_SCREEN))
        self.playButtonImage = pygame.image.load(os.path.join(PLAY_BUTTON_A))
        self.playButtonHoverImage = pygame.image.load(os.path.join(PLAY_BUTTON_HOVER_A))
        self.playButtonClickedImage = pygame.image.load(os.path.join(PLAY_BUTTON_CLICKED_A))
        self.tutorialButtonImage = pygame.image.load(os.path.join(TUTORIAL_BUTTON))
        self.tutorialButtonHoverImage = pygame.image.load(os.path.join(TUTORIAL_BUTTON_HOVER))
        self.tutorialButtonClickedImage = pygame.image.load(os.path.join(TUTORIAL_BUTTON_CLICKED))
        self.optionsButtonImage = pygame.image.load(os.path.join(OPTIONS_BUTTON))
        self.optionsButtonHoverImage = pygame.image.load(os.path.join(OPTIONS_BUTTON_HOVER))
        self.optionsButtonClickedImage = pygame.image.load(os.path.join(OPTIONS_BUTTON_CLICKED))
        self.creditsButtonImage = pygame.image.load(os.path.join(CREDITS_BUTTON))
        self.creditsButtonHoverImage = pygame.image.load(os.path.join(CREDITS_BUTTON_HOVER))
        self.creditsButtonClickedImage = pygame.image.load(os.path.join(CREDITS_BUTTON_CLICKED))
        self.exitButtonImage = pygame.image.load(os.path.join(EXIT_BUTTON))
        self.exitButtonHoverImage = pygame.image.load(os.path.join(EXIT_BUTTON_HOVER))
        self.exitButtonClickedImage = pygame.image.load(os.path.join(EXIT_BUTTON_CLICKED))
        self.buttonImages = (self.playButtonImage, self.tutorialButtonImage, self.optionsButtonImage, self.creditsButtonImage, self.exitButtonImage)
        self.buttonHoverImages = (self.playButtonHoverImage, self.tutorialButtonHoverImage, self.optionsButtonHoverImage, self.creditsButtonHoverImage, self.exitButtonHoverImage)
        self.buttonClickedImages = (self.playButtonClickedImage, self.tutorialButtonClickedImage, self.optionsButtonClickedImage, self.creditsButtonClickedImage, self.exitButtonClickedImage)

    #displays the background of the title screen, was experimental and not being used currently
    #def displayTitleScreenBG(self, screen, numberOfCards, lowerSizeMultiplier, upperSizeMultiplier):
        #for i in range(numberOfCards):
            #sizeMultiplier = random.uniform(lowerSizeMultiplier, upperSizeMultiplier)
            #randomCardColor = random.choice(["red", "blue", "green", "yellow"])
            #randomCardNumber = str(random.randrange(1, 10))
            #randomCardFileName = randomCardColor + "_" + randomCardNumber + ".png"
            #randomCardImage = pygame.image.load(os.path.join('images/cards', randomCardFileName))
            #randomCardImage = pygame.transform.scale(randomCardImage, (randomCardImage.get_width() * sizeMultiplier, randomCardImage.get_height() * sizeMultiplier))
            #xCoord = random.randint(-randomCardImage.get_width()-100, SCREEN_WIDTH+100)
            #yCoord = random.randint(-randomCardImage.get_height()-100, SCREEN_HEIGHT+100)
            #cardSurf = pygame.transform.rotate(randomCardImage, random.randint(0,359))
            #screen.blit(cardSurf, (xCoord, yCoord))
            #pygame.display.update()

    #displays all of the buttons in the title screen
    def displayTitleScreen(self, screen, buttonHovered = -1, buttonClicked = -1):
        screen.blit(self.titleImage, (0,0))

        #checks each of the 5 buttons
        for x in range(len(SETUP_SCREEN_COORDS)):
            if x == buttonHovered:
                screen.blit(self.buttonHoverImages[x], SETUP_SCREEN_COORDS[x])
            elif x == buttonClicked:
                screen.blit(self.buttonClickedImages[x], SETUP_SCREEN_COORDS[x])
            else:
                screen.blit(self.buttonImages[x], SETUP_SCREEN_COORDS[x])
        pygame.display.update()


    #this function displays
    def hoveringOrClickingButtons(self, screen, mousePos, buttonClicked):
        hoveringDisplayed = False

        #checks each of the 5 buttons
        for x in range(5):
            #if mouse is in the area of any of the buttons
            if self.mouseInArea(mousePos, SETUP_SCREEN_COORDS[x], SETUP_SCREEN_BUTTON_SIZES[x]):
                if not buttonClicked:
                    self.displayTitleScreen(screen, x, -1)
                    hoveringDisplayed = True
                elif buttonClicked:
                    self.displayTitleScreen(screen, -1, x)
                    pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
                    return x
        if not hoveringDisplayed:
            self.displayTitleScreen(screen, -1, -1)

        return -1













