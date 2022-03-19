from card import Card
import random
import pygame

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
        # [G1, G2, G3, G4, G5, G6, G7, G8, G9, G10,
        # R1, R2, R3, R4, R5, R6, R7, R8, R9, R10,
        # B1, B2, B3, B4, B5, B6, B7, B8, B9, B10,
        # Y1, Y2, Y3, Y4, Y5, Y6, Y7, Y8, Y9, Y10]
        self.playerNum = playerNum
        if playerNum == 1:
            self.rotationDirection = 0
        elif playerNum == 2:
            self.rotationDirection = 180
        elif playerNum == 3:
            self.rotationDirection = 270
        elif playerNum == 4:
            self.rotationDirection = 90

        self.blitzPile = []  # List of 10 cards
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
        #if the below 5 cards exist, they will be printed to the screen in their designated locations, but only after
        #they are rotated the correct amount for each player
        if self.placePile:
            screen.blit(pygame.transform.rotate(self.placePile[0].image, self.rotationDirection), cardLocations[0])
        if self.blitzPile:
            screen.blit(pygame.transform.rotate(self.blitzPile[0].image, self.rotationDirection), cardLocations[1])
        if self.stackingPiles[0]:
            screen.blit(pygame.transform.rotate(self.stackingPiles[0][0].image, self.rotationDirection), cardLocations[2])
        if self.stackingPiles[1]:
            screen.blit(pygame.transform.rotate(self.stackingPiles[1][0].image, self.rotationDirection), cardLocations[3])
        if self.stackingPiles[2]:
            screen.blit(pygame.transform.rotate(self.stackingPiles[2][0].image, self.rotationDirection), cardLocations[4])

    # given the index, returns a card object if it is there. Otherwise, dont return anything
    def findSelectedCard(self, cardPosIndex):
        if cardPosIndex == 0:
            if len(self.placePile) > 0:
                return self.placePile[0]
        if cardPosIndex == 1:
            if len(self.blitzPile) > 0:
                return self.blitzPile[0]
        if cardPosIndex in range(2, 5):
            if len(self.stackingPiles[cardPosIndex - 2]) > 0:
                return self.stackingPiles[cardPosIndex - 2][0]

    def shuffleDeck(self):
        random.shuffle(self.deck)

    # Creates initial blitz pile and your three initial cards in stacking pile
    def createInitialHand(self, board):
        for x in range(10):
            self.blitzPile.append(self.deck.pop(0))
        self.stackingPiles[0].append(self.deck.pop(0))
        self.stackingPiles[1].append(self.deck.pop(0))
        self.stackingPiles[2].append(self.deck.pop(0))

    # returns true if the card attempted to stack is opposite gender and descending
    # number from the stack pile
    def stackAttempt(self, cardToStack, cardToBePlacedOn):
        if cardToBePlacedOn.gender != (cardToStack.gender):
            if cardToBePlacedOn.number == (cardToStack.number - 1):
                return True
        return False

    def stackResultForStackPile(self, condition, grabbingPileIndex, placingPileIndex):
        # if the stack is valid
        if condition:
            # inserts the top card from the grabbing pile into the placing pile
            (self.stackingPiles[placingPileIndex]).insert(0, self.stackingPiles[grabbingPileIndex][0])
            # removes the "top" element from the grabbing pile
            self.stackingPiles[grabbingPileIndex].pop(0)

            # if the pile that was grabbed from is empty, replace with a card from the blitz pile
            if len(self.stackingPiles[grabbingPileIndex]) == 0:
                (self.stackingPiles[grabbingPileIndex]).insert(0, self.blitzPile[0])
                self.blitzPile.pop(0)

    def stackResultForBlitzPile(self, condition, placingPileIndex):
        # if the stack is valid
        if condition:
            # inserts the top card from the grabbing pile into the placing pile
            (self.stackingPiles[placingPileIndex]).insert(0, self.blitzPile[0])
            # removes the "top" element from the grabbing pile
            self.blitzPile.pop(0)

    def stackResultForPlacePile(self, condition, placingPileIndex):
        # if the stack is valid
        if condition:
            # inserts the top card from the grabbing pile into the placing pile
            (self.stackingPiles[placingPileIndex]).insert(0, self.placePile.pop(0))
            # removes the "top" element from the grabbing pile

    # parameters:
    # stackingPileNum: which stacking pile that the card was taken from
    # gamePileNum: The pile that you are trying to place the card on top of (to gain a point)
    def playAttempt(self, board, gamePileNum, cardToPlay):
        # self.stackingPiles[stackingPileNum][0] is the card at top of stacking pile
        if (cardToPlay.number == 1):
            # if you are trying to place the card on an empty spot in the game board
            if len(board.cardPiles[gamePileNum]) == 0:
                self.score = self.score + 1
                return True
        # if you try to place a card thats not 0 on an empty pile
        elif len(board.cardPiles[gamePileNum]) == 0:
            return False
        # if the color of the cards are the same
        elif cardToPlay.color == board.cardPiles[gamePileNum][0].color:
            # if the number is one greater than the card you are placing on
            if cardToPlay.number == ((board.cardPiles[gamePileNum][0].number) + 1):
                self.score = self.score + 1
                return True

        return False

    def playResultForStackPile(self, condition, board, gamePileNum, grabbingPileIndex):
        if condition:
            # inserts the card onto the spot on the gameboard that was attempted
            board.cardPiles[gamePileNum].insert(0, self.stackingPiles[grabbingPileIndex][0])
            # removes the card from the stackPile
            self.stackingPiles[grabbingPileIndex].pop(0)
            if len(self.stackingPiles[grabbingPileIndex]) == 0:
                if len(self.blitzPile) > 0:
                    (self.stackingPiles[grabbingPileIndex]).insert(0, self.blitzPile.pop(0))

    def playResultForPlacePile(self, condition, board, gamePileNum):
        if condition:
            # inserts the card onto the spot on the gameboard that was attempted
            board.cardPiles[gamePileNum].insert(0, self.placePile.pop(0))
            # removes the card from the stackPile

    def playResultForBlitzPile(self, condition, board, gamePileNum):
        if condition:
            # inserts the card onto the spot on the gameboard that was attempted
            board.cardPiles[gamePileNum].insert(0, self.blitzPile.pop(0))
            # removes the card from the stackPile

    # Flips 3 Cards from player deck and puts them in place pile
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