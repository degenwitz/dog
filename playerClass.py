from board import PlayerGraphic


class PlayerClass():
    def __init__(self):
        self.hand = ()
        self.player_graphic = None

    def getHand(self):
        return  self.hand

    def clearHand(self):
        self.hand = ()

    def set_graphic(self, playerGraphic: PlayerGraphic):
        self.player_graphic = playerGraphic

    def removeCard(self, card, allertGraphic=True):
        handList = list(self.hand)
        handList.remove(card)
        self.hand = tuple(handList)
        if allertGraphic and self.player_graphic != None:
            self.player_graphic.remove_card(card)

    def addCard(self, card, allertGraphic=True):
        self.hand = self.hand + (card,)
        if allertGraphic and self.player_graphic != None:
            #self.player_graphic.add_card(card)
            pass

    def newHand(self, hand):
        self.hand = hand