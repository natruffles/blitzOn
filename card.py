import pygame
import os

class Card():
  def __init__(self, color, number, gender, fileName, x, y):
    self.color = color
    self.number = number
    self.gender = gender
    self.fileName = fileName
    self.image = pygame.image.load(os.path.join('images/cards', self.fileName))
    self.isSelected = False
    self.location = (x, y)