import pygame

class Sounds():
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.7)
        self.buttonClick = pygame.mixer.Sound("sounds/buttonClick.mp3")
        self.cardPlace = pygame.mixer.Sound("sounds/cardPlace.mp3")
        self.win = pygame.mixer.Sound("sounds/tada.mp3")
        self.lose = pygame.mixer.Sound("sounds/loss.mp3")

