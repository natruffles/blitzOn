import pygame
import os
from constants import *
from gameBoard import GameBoard
from player import Player
from ai import AI

##################################################################################
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/buttonClick.mp3")
pygame.mixer.music.set_volume(0.7)
font = pygame.font.SysFont("comicsansms", 48)

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


##################################################################################


# Determines whether the players mouse is on one
# of their cards, will return which card and T/F
# in a tuple. EX (3, True)
def hoveringOverACardForPickup(mouseX, mouseY, playerCoords):
    for i in range(len(playerCoords)):
        cardX = playerCoords[i][0]
        cardY = playerCoords[i][1]
        if mouseX >= cardX and mouseX <= cardX + CARD_SIZE_X and mouseY >= cardY and mouseY <= cardY + CARD_SIZE_Y:
            return i
    return -1


def hoveringOverACardForPlaceDown(mouseX, mouseY, placeDownCoords):
    for i in range(len(placeDownCoords)):
        cardX = placeDownCoords[i][0]
        cardY = placeDownCoords[i][1]
        if mouseX >= cardX and mouseX <= cardX + CARD_SIZE_X and mouseY >= cardY and mouseY <= cardY + CARD_SIZE_Y:
            return i
    return -1


# Checks to see if a button has been pressed
# Int Int Tuple(2) Tuple(2)
def hasButtonBeenPressed(mouseX, mouseY, buttonCoords, buttonSize):
    if mouseX in range(buttonCoords[0], buttonCoords[0] + buttonSize[0]):
        if mouseY in range(buttonCoords[1], buttonCoords[1] + buttonSize[1]):
            return True
    return False


def main():
    ##0 is for light mode, 1 is for dark mode
    darkOrLightState = 0

    board = [GameBoard(GAME_BOARD_IMAGES[0], SCREEN_WIDTH, SCREEN_HEIGHT),
             GameBoard(GAME_BOARD_IMAGES[1], SCREEN_WIDTH, SCREEN_HEIGHT)]

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

    runTitleScreen = True
    runGame = True

    clock = pygame.time.Clock()
    darkOrLightState = 0

    while runTitleScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGame = False
                pygame.quit()

        clock.tick(30)
        screen.fill((0, 0, 0))
        screen.blit(titleImage, (0, 0))
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
        board[darkOrLightState].displayCardPiles(screen, PILE_CARD_COORDS)

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

            # if the mouse is on top of a valid card spot (index 0-4)
            if player1.selectedCardIndexOnGameBoard in range(0, 5):
                # if there is a card to select
                if (player1.findSelectedCard(player1.selectedCardIndexOnGameBoard)):
                    # card object stored
                    player1.selectedCard = player1.findSelectedCard(player1.selectedCardIndexOnGameBoard)
                    player1.cardSelected = True
            # Checks to see if mouse clicked the flip button
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

        # if the mouse is clicked and a card is selected, it will try to place the card down
        if pygame.mouse.get_pressed(3)[0] and player1.cardSelected:
            mousePos = pygame.mouse.get_pos()
            placeDownPosIndex = hoveringOverACardForPlaceDown(mousePos[0], mousePos[1], PILE_CARD_COORDS)
            # Returns index of stacking pile you are trying to place on top of
            stackingPosIndex = hoveringOverACardForPickup(mousePos[0], mousePos[1], P1_CARD_COORDS)

            # if hovering over cards on the game pile
            if placeDownPosIndex in range(0, 12):
                # if the play attempt is valid
                if player1.playAttempt(board[darkOrLightState], placeDownPosIndex, player1.selectedCard):
                    if player1.selectedCardIndexOnGameBoard in range(2, 5):
                        player1.playResultForStackPile(True, board[darkOrLightState], placeDownPosIndex,
                                                       (player1.selectedCardIndexOnGameBoard - 2))
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

            # if hovering over cards in the stacking pile
            elif stackingPosIndex in range(2, 5):
                if player1.stackAttempt(player1.stackingPiles[stackingPosIndex - 2][0], player1.selectedCard):
                    if player1.selectedCardIndexOnGameBoard in range(2, 5):
                        player1.stackResultForStackPile(True, player1.selectedCardIndexOnGameBoard - 2,
                                                        stackingPosIndex - 2)
                    if player1.selectedCardIndexOnGameBoard == 0:
                        player1.stackResultForPlacePile(True, stackingPosIndex - 2)
                    if player1.selectedCardIndexOnGameBoard == 1:
                        player1.stackResultForBlitzPile(True, stackingPosIndex - 2)
                    pygame.mixer.music.pause()
                    pygame.mixer.music.load("sounds/cardPlace.mp3")
                    pygame.mixer.music.play()
                    player1.selectedCardIndexOnGameBoard = -1
                    player1.cardSelected = False
                    pygame.time.wait(250)

        if pygame.mouse.get_pressed(3)[2]:
            player1.selectedCardIndexOnGameBoard = -1
            player1.cardSelected = False

        # if the card is selected, the card will move around the screen with the cursor
        if player1.cardSelected:
            mousePos = pygame.mouse.get_pos()
            clickedCardPos = (mousePos[0] - 74 / 2, mousePos[1] - 108 / 2)
            screen.blit(player1.selectedCard.image, clickedCardPos)

        player2.playCards(board[darkOrLightState])
        player3.playCards(board[darkOrLightState])
        player4.playCards(board[darkOrLightState])

        # checks for and removes piles of 10 from the game board
        board[darkOrLightState].checkForPilesToRemove()

        pygame.display.update()

        if len(player1.blitzPile) == 0 or len(player2.blitzPile) == 0 or len(player3.blitzPile) == 0 or len(
                player4.blitzPile) == 0:
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
        board[darkOrLightState].displayCardPiles(screen, PILE_CARD_COORDS)

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
