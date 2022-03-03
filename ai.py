from player import Player

class AI(Player):
    def __init__(self, playerNum):
        super().__init__(playerNum)

    # whenever you use self.playAttempt, gamePileNum is 0-11
    # def playAttempt(self, board, gamePileNum, cardToPlay)
    def playCards(self, board):
        go_again = True
        while go_again:
            go_again = False

            # go through the blitz pile
            for x in range(0, 12):
                if len(self.blitzPile) > 0:
                    if self.playAttempt(board, x, self.blitzPile[0]):
                        self.playResultForBlitzPile(True, board, x)
                        go_again = True

            # go through the stack pile
            for index in range(0, 3):
                for x in range(0, 12):
                    if len(self.stackingPiles[index]) > 0:
                        if self.playAttempt(board, x, self.stackingPiles[index][0]):
                            self.playResultForStackPile(True, board, x, index)
                            go_again = True

            # go through the flip pile
            for x in range(0, 12):
                if len(self.placePile) > 0:
                    if self.playAttempt(board, x, self.placePile[0]):
                        self.playResultForPlacePile(True, board, x)
                        go_again = True

