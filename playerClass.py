

class PlayerClass():
    def __init__(self):
        self.hand = ()

    def getHand(self):
        return  self.hand

    def clearHand(self):
        self.hand = ()

    def removeCard(self, card):
        handList = list(self.hand)
        handList.remove(card)
        self.hand = tuple(handList)

    def addCard(self, card):
        self.hand = self.hand + (card,)

    def newHand(self, hand):
        self.hand = hand