import pygame
import math
import random
import os

##################################################################################
##################################################################################
##################################################################################
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/buttonClick.mp3")
#pygame.mixer.music.load("sounds/cardPlace.mp3")
#pygame.mixer.music.load("sounds/tada.mp3")
pygame.mixer.music.set_volume(0.7)
font = pygame.font.SysFont("comicsansms", 48)


# Constants used
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
AI_WAIT_TIME = 1500

#Gameboard file name
GAME_BOARD_IMAGES = ["board_v3.png", "board_v3_b.png"]
TITLE_SCREEN = "title_screen.png"
END_SCREENS = ["win_notification.png", "lose_notification.png"]
PLAY_BUTTON = "play_button_a.png"
PLAY_BUTTON_CLICKED = "play_button_b.png"
DARK_BUTTON = "dark_button_a.png"
DARK_BUTTON_CLICKED = "dark_button_b.png"
LIGHT_BUTTON = "light_button_a.png"
LIGHT_BUTTON_CLICKED = "light_button_b.png"
READY_BUTTON = "ready_button_a.png"
READY_BUTTON_CLICKED = "ready_button_b.png"

titleImage = pygame.image.load(os.path.join('images', TITLE_SCREEN))
winImage = pygame.image.load(os.path.join('images', END_SCREENS[0]))
loseImage = pygame.image.load(os.path.join('images', END_SCREENS[1]))
playButtonImage = pygame.image.load(os.path.join('images/buttons', PLAY_BUTTON))
playButtonClickedImage = pygame.image.load(os.path.join('images/buttons', PLAY_BUTTON_CLICKED))
darkButtonImage = pygame.image.load(os.path.join('images/buttons', DARK_BUTTON))
darkButtonClickedImage = pygame.image.load(os.path.join('images/buttons', DARK_BUTTON_CLICKED))
lightButtonImage = pygame.image.load(os.path.join('images/buttons', LIGHT_BUTTON))
lightButtonClickedImage = pygame.image.load(os.path.join('images/buttons', LIGHT_BUTTON_CLICKED))
ReadyButtonImage = pygame.image.load(os.path.join('images/buttons', READY_BUTTON))
ReadyButtonClickedImage = pygame.image.load(os.path.join('images/buttons', READY_BUTTON_CLICKED))


P1_CARD_COORDS = [(195, 601), (280, 601) , (363, 601) , (445, 601) , (527, 601)]
P2_CARD_COORDS = [(526, 8), (445, 8) , (363, 8) , (280, 8) , (195, 8)]
P3_CARD_COORDS = [(14, 35), (14, 149) , (14, 263) , (14, 377) , (14, 491)]
P4_CARD_COORDS = [(699, 491), (699, 377) , (699, 263) , (699, 149) , (699, 35)]

PILE_CARD_COORDS = [(237, 179), (320, 179), (402, 179), (483, 179), (237, 298), (320, 298), (402, 298), (483, 298), (237, 421), (320, 421), (402, 421), (483, 421)]

READY_BUTTON_COORDS = (790, 621)
READY_BUTTON_SIZE = (354, 95)

PLAY_BUTTON_COORDS = (86, 441)
PLAY_BUTTON_SIZE = (478, 246)

DARK_LIGHT_BUTTON_COORDS = (676, 441)
DARK_LIGHT_BUTTON_SIZE = (478, 246)

BUTTON_PRESS_ANIMATION_DELAY = 250

BLITZ_SCORE_COORDS = [(874,29), (874,87), (874, 145), (874,203)]
PLAYED_SCORE_COORDS = [(1138, 29), (1138, 87), (1138, 145), (1138, 203)]

END_MESSAGE_COORDS = (840,340)



##################################################################################
##################################################################################
##################################################################################


class Card():
  def __init__(self, color, number, gender, fileName, x, y):
    self.color = color
    self.number = number
    self.gender = gender
    self.fileName = fileName
    self.image = pygame.image.load(os.path.join('images/cards', self.fileName))
    self.isSelected = False
    self.location = (x, y)

class GameBoard():
    def __init__(self, fileName):
      self.screenWidth = SCREEN_WIDTH
      self.screenHeight = SCREEN_HEIGHT
      self.boardFileName = fileName
      self.boardImage = pygame.image.load(os.path.join('images', self.boardFileName))
      self.cardPiles = [[],[],[],[],[],[],[],[],[],[],[],[]]   #list of up to 12 piles of cards (with up to 10 cards per pile)
      self.usedCards = []   #list of cards

    #checks for and removes piles of 10 from the game board
    def checkForPilesToRemove(self):
      for x in range(len(self.cardPiles)):
        if len(self.cardPiles[x]) > 0:
          if (self.cardPiles[x][0].number == 10):
            for y in range(len(self.cardPiles[x])):
              self.usedCards.append(self.cardPiles[x].pop(0))
            self.cardPiles[x] = []

    def displayCardPiles(self, screen):
      for x in range(len(self.cardPiles)):
        if len(self.cardPiles[x]) > 0:
          screen.blit(self.cardPiles[x][0].image, PILE_CARD_COORDS[x])




class Player():
  def __init__(self, playerNum):
    self.score = 0
    self.deck = []
    for i in range(0, 10):
        self.deck.append(Card("G", i + 1, "F", "green_" + str(i + 1) + ".png", 0, 0))
    for i in range(10, 20):
        self.deck.append(Card("Y", i + 1 - 10, "F", "yellow_" + str(i + 1 - 10) + ".png", 0, 0))
    for i in range(20, 30):
        self.deck.append(Card("R", i + 1 - 20, "M", "red_" + str(i + 1 - 20) + ".png", 0, 0))
    for i in range(30, 40):
        self.deck.append(Card("B", i + 1 - 30, "M", "blue_" + str(i + 1 - 30) + ".png", 0, 0))
    #[G1, G2, G3, G4, G5, G6, G7, G8, G9, G10,
                #R1, R2, R3, R4, R5, R6, R7, R8, R9, R10,
                #B1, B2, B3, B4, B5, B6, B7, B8, B9, B10,
                #Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8, Y9, Y10]
    self.playerNum = playerNum
    self.blitzPile = []            #List of 10 cards
    self.stacking1 = []            
    self.stacking2 = []
    self.stacking3 = []
    self.stackingPiles = [self.stacking1, self.stacking2, self.stacking3]
    self.placePile = []
    self.cardSelected = False
    self.selectedCard = 0
    self.selectedCardIndexOnGameBoard = -1

  # self{}, screen{surface}, cardLocations{list of 5 tuples}
  def displayPlayerCards(self, screen, cardLocations):
    if self.placePile:
        screen.blit(self.placePile[0].image, cardLocations[0])
    if self.blitzPile:
        screen.blit(self.blitzPile[0].image, cardLocations[1])
    if self.stackingPiles[0]:
        screen.blit(self.stackingPiles[0][0].image, cardLocations[2])
    if self.stackingPiles[1]:
        screen.blit(self.stackingPiles[1][0].image, cardLocations[3])
    if self.stackingPiles[2]:
        screen.blit(self.stackingPiles[2][0].image, cardLocations[4])

  #given the index, returns a card object if it is there. Otherwise, dont return anything
  def findSelectedCard(self, cardPosIndex):
    if cardPosIndex == 0:
      if len(self.placePile) > 0:  
        return self.placePile[0]
    if cardPosIndex == 1:
      if len(self.blitzPile) > 0:
        return self.blitzPile[0]
    if cardPosIndex in range(2,5):
      if len(self.stackingPiles[cardPosIndex-2]) > 0:
        return self.stackingPiles[cardPosIndex-2][0]
    
  
  def shuffleDeck(self):
    random.shuffle(self.deck)

  # Creates initial blitz pile and your three initial cards in stacking pile
  def createInitialHand(self, board):
    for x in range(10):
      self.blitzPile.append(self.deck.pop(0))
    self.stackingPiles[0].append(self.deck.pop(0))
    self.stackingPiles[1].append(self.deck.pop(0))
    self.stackingPiles[2].append(self.deck.pop(0))
          

  #places 3 cards in the placePile
  def placeCardsInPile(self):
    for x in range(3):
      self.placePile.insert(0,(self.deck.pop(0)))

  #returns true if the card attempted to stack is opposite gender and descending 
  #number from the stack pile
  def stackAttempt(self, cardToStack, cardToBePlacedOn):
    if cardToBePlacedOn.gender != (cardToStack.gender):
      if cardToBePlacedOn.number == (cardToStack.number - 1):
        return True
    
    return False

  def stackResultForStackPile(self, condition, grabbingPileIndex, placingPileIndex):
    #if the stack is valid
    if condition:
      #inserts the top card from the grabbing pile into the placing pile
      (self.stackingPiles[placingPileIndex]).insert(0, self.stackingPiles[grabbingPileIndex][0])
      #removes the "top" element from the grabbing pile
      self.stackingPiles[grabbingPileIndex].pop(0)

      #if the pile that was grabbed from is empty, replace with a card from the blitz pile
      if len(self.stackingPiles[grabbingPileIndex]) == 0:
        (self.stackingPiles[grabbingPileIndex]).insert(0, self.blitzPile[0])
        self.blitzPile.pop(0)


  def stackResultForBlitzPile(self, condition, placingPileIndex):
    #if the stack is valid
    if condition:
      #inserts the top card from the grabbing pile into the placing pile
      (self.stackingPiles[placingPileIndex]).insert(0, self.blitzPile[0])
      #removes the "top" element from the grabbing pile
      self.blitzPile.pop(0)

  def stackResultForPlacePile(self, condition, placingPileIndex):
    #if the stack is valid
    if condition:
      #inserts the top card from the grabbing pile into the placing pile
      (self.stackingPiles[placingPileIndex]).insert(0, self.placePile.pop(0))
      #removes the "top" element from the grabbing pile
      

  #parameters:
    #stackingPileNum: which stacking pile that the card was taken from
    #gamePileNum: The pile that you are trying to place the card on top of (to gain a point)
  def playAttempt(self, board, gamePileNum, cardToPlay):
    #self.stackingPiles[stackingPileNum][0] is the card at top of stacking pile
    if (cardToPlay.number == 1):
      #if you are trying to place the card on an empty spot in the game board
      if len(board.cardPiles[gamePileNum]) == 0:
        self.score = self.score + 1
        return True
    #if you try to place a card thats not 0 on an empty pile
    elif len(board.cardPiles[gamePileNum]) == 0:
      return False
    #if the color of the cards are the same
    elif cardToPlay.color == board.cardPiles[gamePileNum][0].color:
      #if the number is one greater than the card you are placing on
      if cardToPlay.number == ((board.cardPiles[gamePileNum][0].number) + 1):
        self.score = self.score + 1
        return True

    return False

  def playResultForStackPile(self, condition, board, gamePileNum, grabbingPileIndex):
    if condition:
      #inserts the card onto the spot on the gameboard that was attempted
      board.cardPiles[gamePileNum].insert(0, self.stackingPiles[grabbingPileIndex][0])
      #removes the card from the stackPile
      self.stackingPiles[grabbingPileIndex].pop(0)
      if len(self.stackingPiles[grabbingPileIndex]) == 0:
        if len(self.blitzPile) > 0:
          (self.stackingPiles[grabbingPileIndex]).insert(0, self.blitzPile.pop(0))
        



  def playResultForPlacePile(self, condition, board, gamePileNum):
    if condition:
      #inserts the card onto the spot on the gameboard that was attempted
      board.cardPiles[gamePileNum].insert(0, self.placePile.pop(0))
      #removes the card from the stackPile
      

  def playResultForBlitzPile(self, condition, board, gamePileNum):
    if condition:
      #inserts the card onto the spot on the gameboard that was attempted
      board.cardPiles[gamePileNum].insert(0, self.blitzPile.pop(0))
      #removes the card from the stackPile
      

  #Flips 3 Cards from player deck and puts them in place pile
  def flipPlacePile(self):
    if len(self.deck) < 1:
      self.deck = self.placePile
      self.deck.reverse()
      self.placePile = []
    if len(self.deck) < 3:
      for i in range(len(self.deck)):
        self.placePile.insert(0, self.deck.pop(0))
    else:
      for i in range(3):
        self.placePile.insert(0, self.deck.pop(0))
    
      
class AI(Player):
  def __init__(self, playerNum):
    super().__init__(playerNum)

  #whenever you use self.playAttempt, gamePileNum is 0-11
  #def playAttempt(self, board, gamePileNum, cardToPlay)
  def playCards(self, board):
    go_again = True
    while go_again:
      go_again = False
      
      # go through the blitz pile
      for x in range (0,12):
        if len(self.blitzPile) > 0:
          if self.playAttempt(board, x, self.blitzPile[0]):
            self.playResultForBlitzPile(True, board, x)
            go_again = True

      # go through the stack pile
      for index in range(0,3):
        for x in range (0,12):
          if len(self.stackingPiles[index]) > 0:
            if self.playAttempt(board, x, self.stackingPiles[index][0]):
              self.playResultForStackPile(True, board, x, index)
              go_again = True

      # go through the flip pile
      for x in range (0,12):
        if len(self.placePile) > 0:
          if self.playAttempt(board, x, self.placePile[0]):
            self.playResultForPlacePile(True, board, x)
            go_again = True
        
    


##################################################################################
##################################################################################
##################################################################################


#Determines whether the players mouse is on one
# of their cards, will return which card and T/F
# in a tuple. EX (3, True)
def hoveringOverACardForPickup(mouseX, mouseY, playerCoords):
  rectsizeX = 74
  rectsizeY = 108
  for i in range(len(playerCoords)):
    cardX = playerCoords[i][0]
    cardY = playerCoords[i][1]
    if mouseX >= cardX and mouseX <= cardX + rectsizeX and mouseY >= cardY and mouseY <= cardY + rectsizeY:
      return i
  return -1

def hoveringOverACardForPlaceDown(mouseX, mouseY, placeDownCoords):
  rectsizeX = 74
  rectsizeY = 108
  for i in range(len(placeDownCoords)):
    cardX = placeDownCoords[i][0]
    cardY = placeDownCoords[i][1]
    if mouseX >= cardX and mouseX <= cardX + rectsizeX and mouseY >= cardY and mouseY <= cardY + rectsizeY:
      return i
  return -1

# Checks to see if a button has been pressed
# Int Int Tuple(2) Tuple(2)
def hasButtonBeenPressed(mouseX, mouseY, buttonCoords, buttonSize):
  if mouseX in range(buttonCoords[0], buttonCoords[0] + buttonSize[0]):
    if mouseY in range(buttonCoords[1], buttonCoords[1] + buttonSize[1]):
      return True
  return False

global darkOrLightState
##0 is for light mode, 1 is for dark mode
darkOrLightState = 0
board = [GameBoard(GAME_BOARD_IMAGES[0]), GameBoard(GAME_BOARD_IMAGES[1])]

screen = pygame.display.set_mode((board[darkOrLightState].screenWidth, board[darkOrLightState].screenHeight))

pygame.display.set_caption("BlitzOn!")


player1 = Player(1)
player1.shuffleDeck()
player1.createInitialHand(board[darkOrLightState])

player2 = AI(2)
player2.shuffleDeck()
player2.createInitialHand(board[darkOrLightState])

player3 = AI(3)
player3.shuffleDeck()
player3.createInitialHand(board[darkOrLightState])

player4 = AI(4)
player4.shuffleDeck()
player4.createInitialHand(board[darkOrLightState])



def main():
  runTitleScreen = True
  runGame = True

  clock = pygame.time.Clock()
  clickedCardPos = (0,0)
  darkOrLightState = 0

  while runTitleScreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
            pygame.quit()

    clock.tick(30)
    screen.fill((0,0,0))
    screen.blit(titleImage, (0,0))
    screen.blit(playButtonImage, PLAY_BUTTON_COORDS)

    if darkOrLightState == 0:
      screen.blit(darkButtonImage, DARK_LIGHT_BUTTON_COORDS)
    else:
      screen.blit(lightButtonImage, DARK_LIGHT_BUTTON_COORDS)


    if pygame.mouse.get_pressed(3)[0]:
      mousePos = pygame.mouse.get_pos()
      if hasButtonBeenPressed(mousePos[0], mousePos[1], PLAY_BUTTON_COORDS, PLAY_BUTTON_SIZE):
        pygame.mixer.music.pause()
        pygame.mixer.music.load("sounds/buttonClick.mp3")
        pygame.mixer.music.play()
        screen.blit(playButtonClickedImage, PLAY_BUTTON_COORDS)
        pygame.display.update()
        pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
        runTitleScreen = False
      if hasButtonBeenPressed(mousePos[0], mousePos[1], DARK_LIGHT_BUTTON_COORDS, DARK_LIGHT_BUTTON_SIZE):
        pygame.mixer.music.pause()
        pygame.mixer.music.load("sounds/buttonClick.mp3")
        pygame.mixer.music.play()
        if darkOrLightState == 0:
          screen.blit(darkButtonClickedImage, DARK_LIGHT_BUTTON_COORDS)
          pygame.display.update()
          pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
          screen.blit(lightButtonImage, DARK_LIGHT_BUTTON_COORDS)
          pygame.display.update()
          darkOrLightState = 1
        else:
          screen.blit(lightButtonClickedImage, DARK_LIGHT_BUTTON_COORDS)
          pygame.display.update()
          pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
          screen.blit(darkButtonImage, DARK_LIGHT_BUTTON_COORDS)
          pygame.display.update()
          darkOrLightState = 0

    pygame.display.update()


      
      

  
  while runGame:
    clock.tick(30)

    screen.fill((0, 0, 0))
    screen.blit(board[darkOrLightState].boardImage, (0, 0))
    screen.blit(ReadyButtonImage, READY_BUTTON_COORDS)
    player1.displayPlayerCards(screen, P1_CARD_COORDS)
    player2.displayPlayerCards(screen, P2_CARD_COORDS)
    player3.displayPlayerCards(screen, P3_CARD_COORDS)
    player4.displayPlayerCards(screen, P4_CARD_COORDS)
    board[darkOrLightState].displayCardPiles(screen)

    text = font.render(str(len(player1.blitzPile)), True, (0, 0, 0))
    screen.blit(text, BLITZ_SCORE_COORDS[0])
    text = font.render(str(len(player2.blitzPile)), True, (0, 0, 0))
    screen.blit(text, (BLITZ_SCORE_COORDS[1]))
    text = font.render(str(len(player3.blitzPile)), True, (0, 0, 0))
    screen.blit(text, (BLITZ_SCORE_COORDS[2]))
    text = font.render(str(len(player4.blitzPile)), True, (0, 0, 0))
    screen.blit(text, (BLITZ_SCORE_COORDS[3]))

    text = font.render(str(player1.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[0]))
    text = font.render(str(player2.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[1]))
    text = font.render(str(player3.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[2]))
    text = font.render(str(player4.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[3]))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
            pygame.quit()

    # if the mouse is clicked and no card is selected
    if pygame.mouse.get_pressed(3)[0] and player1.selectedCardIndexOnGameBoard == -1:
      mousePos = pygame.mouse.get_pos()
      player1.selectedCardIndexOnGameBoard = hoveringOverACardForPickup(mousePos[0], mousePos[1], P1_CARD_COORDS)
      

      #if the mouse is on top of a valid card spot (index 0-4)
      if player1.selectedCardIndexOnGameBoard in range(0,5):
        #if there is a card to select
        if (player1.findSelectedCard(player1.selectedCardIndexOnGameBoard)):
          #card object stored
          player1.selectedCard = player1.findSelectedCard(player1.selectedCardIndexOnGameBoard)
          player1.cardSelected = True
      #Checks to see if mouse clicked the flip button
      elif hasButtonBeenPressed(mousePos[0], mousePos[1], READY_BUTTON_COORDS, READY_BUTTON_SIZE):
        pygame.mixer.music.pause()
        pygame.mixer.music.load("sounds/buttonClick.mp3")
        pygame.mixer.music.play()
        
        
     
        
        screen.blit(ReadyButtonClickedImage, READY_BUTTON_COORDS)
        pygame.display.update()
        pygame.time.wait(BUTTON_PRESS_ANIMATION_DELAY)
        screen.blit(ReadyButtonImage, READY_BUTTON_COORDS)
        pygame.display.update()
        player1.flipPlacePile()
        player2.flipPlacePile()
        player3.flipPlacePile()
        player4.flipPlacePile()

    #if the mouse is clicked and a card is selected, it will try to place the card down
    if pygame.mouse.get_pressed(3)[0] and player1.cardSelected:
      mousePos = pygame.mouse.get_pos()
      placeDownPosIndex = hoveringOverACardForPlaceDown(mousePos[0], mousePos[1], PILE_CARD_COORDS)
      #Returns index of stacking pile you are trying to place on top of
      stackingPosIndex = hoveringOverACardForPickup(mousePos[0], mousePos[1], P1_CARD_COORDS)

      #if hovering over cards on the game pile
      if placeDownPosIndex in range(0,12):
        #if the play attempt is valid
        if player1.playAttempt(board[darkOrLightState], placeDownPosIndex, player1.selectedCard):
          if player1.selectedCardIndexOnGameBoard in range(2,5):
            player1.playResultForStackPile(True, board[darkOrLightState], placeDownPosIndex, (player1.selectedCardIndexOnGameBoard-2))
          if player1.selectedCardIndexOnGameBoard == 0:
            player1.playResultForPlacePile(True, board[darkOrLightState], placeDownPosIndex)
          if player1.selectedCardIndexOnGameBoard == 1:
            player1.playResultForBlitzPile(True, board[darkOrLightState], placeDownPosIndex)
          pygame.mixer.music.pause()
          pygame.mixer.music.load("sounds/cardPlace.mp3")
          pygame.mixer.music.play()
          player1.selectedCardIndexOnGameBoard = -1
          player1.cardSelected = False
          pygame.time.wait(250)

      #if hovering over cards in the stacking pile
      elif stackingPosIndex in range(2,5):
        if player1.stackAttempt(player1.stackingPiles[stackingPosIndex-2][0], player1.selectedCard):
          if player1.selectedCardIndexOnGameBoard in range(2,5):
            player1.stackResultForStackPile(True, player1.selectedCardIndexOnGameBoard-2, stackingPosIndex-2)
          if player1.selectedCardIndexOnGameBoard == 0:
            player1.stackResultForPlacePile(True, stackingPosIndex-2)
          if player1.selectedCardIndexOnGameBoard == 1:
            player1.stackResultForBlitzPile(True, stackingPosIndex-2)
          pygame.mixer.music.pause()
          pygame.mixer.music.load("sounds/cardPlace.mp3")
          pygame.mixer.music.play()
          player1.selectedCardIndexOnGameBoard = -1
          player1.cardSelected = False
          pygame.time.wait(250)

       
    if pygame.mouse.get_pressed(3)[2]:
      player1.selectedCardIndexOnGameBoard = -1
      player1.cardSelected = False
          
    #if the card is selected, the card will move around the screen with the cursor
    if player1.cardSelected:
      mousePos = pygame.mouse.get_pos()
      clickedCardPos = (mousePos[0] - 74/2, mousePos[1] - 108/2)
      screen.blit(player1.selectedCard.image, clickedCardPos)

    player2.playCards(board[darkOrLightState])
    player3.playCards(board[darkOrLightState])
    player4.playCards(board[darkOrLightState])

    #checks for and removes piles of 10 from the game board
    board[darkOrLightState].checkForPilesToRemove()
    
    pygame.display.update()
      
    if len(player1.blitzPile) == 0 or len(player2.blitzPile) == 0 or len(player3.blitzPile) == 0 or len(player4.blitzPile) == 0:
      runGame = False

  # Displays whether the user wins or loses based on which players blitz pile ran out first
  while runGame == False:
    screen.fill((0, 0, 0))
    screen.blit(board[darkOrLightState].boardImage, (0, 0))
    screen.blit(ReadyButtonImage, READY_BUTTON_COORDS)
    player1.displayPlayerCards(screen, P1_CARD_COORDS)
    player2.displayPlayerCards(screen, P2_CARD_COORDS)
    player3.displayPlayerCards(screen, P3_CARD_COORDS)
    player4.displayPlayerCards(screen, P4_CARD_COORDS)
    board[darkOrLightState].displayCardPiles(screen)

    text = font.render(str(len(player1.blitzPile)), True, (0, 0, 0))
    screen.blit(text, BLITZ_SCORE_COORDS[0])
    text = font.render(str(len(player2.blitzPile)), True, (0, 0, 0))
    screen.blit(text, (BLITZ_SCORE_COORDS[1]))
    text = font.render(str(len(player3.blitzPile)), True, (0, 0, 0))
    screen.blit(text, (BLITZ_SCORE_COORDS[2]))
    text = font.render(str(len(player4.blitzPile)), True, (0, 0, 0))
    screen.blit(text, (BLITZ_SCORE_COORDS[3]))

    text = font.render(str(player1.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[0]))
    text = font.render(str(player2.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[1]))
    text = font.render(str(player3.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[2]))
    text = font.render(str(player4.score), True, (0, 0, 0))
    screen.blit(text, (PLAYED_SCORE_COORDS[3]))

    if player1.score - len(player1.blitzPile) >= player2.score - len(player2.blitzPile) \
      and player1.score - len(player1.blitzPile) >= player3.score - len(player3.blitzPile) \
      and player1.score - len(player1.blitzPile) >= player4.score - len(player4.blitzPile):

      screen.blit(winImage, END_MESSAGE_COORDS)
      text = font.render(str(len(player1.blitzPile)), True, (0, 0, 0))
      screen.blit(text, BLITZ_SCORE_COORDS[0])
      pygame.display.update()
      pygame.mixer.music.pause()
      pygame.mixer.music.load("sounds/tada.mp3")
      pygame.mixer.music.play()
      pygame.time.wait(10000)
      runGame = True
      pygame.quit()
    else:
      screen.blit(loseImage, END_MESSAGE_COORDS)
      pygame.display.update()
      pygame.mixer.music.pause()
      pygame.mixer.music.load("sounds/loss.mp3")
      pygame.mixer.music.play()
      pygame.time.wait(10000)
      runGame = True
      pygame.quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

main()
