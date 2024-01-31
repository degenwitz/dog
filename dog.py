from board import (FigureButton, BoardGraphic)
from boardDTO import Board
from PyQt5.QtWidgets import QApplication
from playerClass import PlayerClass
from randomPlayer import RandomPlayerBot
from Cards import Card, EasyCard, Four, Seven, King, Ass, Joker
import random
from global_vals import spielfeld, zuhause, ziele
from Figure import Figur
from Game import Game

numernKarten = (2,3,4,5,6,8,9,10,12)
colors = ( "♣", "♢", "♡", "♠")

class GameRunner():

    def __init__(self, playerBot1, playerBot2, playerBot3, playerBot4):
        self.playersBots = [playerBot1, playerBot2, playerBot3, playerBot4]
        self.players = (PlayerClass(), PlayerClass(), PlayerClass(), PlayerClass())
        self.currentPlayer = 0
        self.currentHandSize = 6
        self.deck = GameRunner.deckBauen()
        self.discard = ()
    
    def deckBauen():
        deck = []
        for j in range(2):
            for color in colors:
                for num in numernKarten:
                    deck.append(EasyCard(color, num))
                deck.append(Four(color))
                deck.append(Seven(color))
                deck.append(King(color))
                deck.append(Ass(color))
            for i in range(3):
                deck.append(Joker())
        random.shuffle(deck)
        return tuple(deck)

    def deckReshuffle(self):
        if(len(self.deck) == 0):
            deck = list(self.discard)
            random.shuffle(deck)
            self.deck = tuple(deck)
            self.discard = ()

    def distributeCards(self):
        for i in range(self.currentHandSize):
            for j in range(4):
                self.deckReshuffle()
                self.players[(self.currentPlayer+j)%4].addCard(self.deck[0])
                self.boardGraphic.addCard(self.deck[0],("player", j))
                self.deck = self.deck[1:]

        #for j in range(4):
            #self.players[(self.currentPlayer + j) % 4].addCard(Ass("♣")) ##TODO: Remove this, only for testing

        self.currentHandSize -= 1
        if self.currentHandSize < 2:
            self.currentHandSize = 5

    def executeCard(self, playerNumber, card):
        if isinstance(card, King):
            for figs in self.boardGraphic.getFigures():
                if figs.get_spielernummer() == playerNumber:
                    if figs.get_aktuelles_feld()[0] in zuhause:
                        figs.rauskommen()
                        return
        if isinstance(card, EasyCard) and card.get_target_figure() != None:
            figure = self.boardGraphic.getFigure(card.get_target_figure(),playerNumber)
            figure.ziehen(card.get_value(), card.get_enter_if_possible() )

    def nextMove(self):
        cards = self.players[self.currentPlayer].getHand()
        if len(cards) != 0:
            print(self.currentPlayer)
            board, figuren, game = self.generatePlayerObjects(self.currentPlayer)
            playedCard = self.playersBots[self.currentPlayer].playCard(cards, board, figuren, game)
            self.executeCard(self.currentPlayer, playedCard)
            self.players[self.currentPlayer].removeCard(playedCard)
            self.discard += (playedCard,)
        self.currentPlayer = (self.currentPlayer + 1)%4

    def setGraphicBoard(self, boardGraphic):
        self.boardGraphic = boardGraphic

    def generatePlayerObjects(self, playerNumber):
        figuresGr = self.boardGraphic.getFigures()
        figuren = []
        for figure in figuresGr:
            feldGr = figure.get_aktuelles_feld()
            feld = feldGr
            if spielfeld == feldGr[0]:
                feld = (spielfeld, (feldGr[1]-playerNumber*16)%(16*4) )
            for heim in zuhause:
                if heim == feldGr[0]:
                    spielernummer = int(heim[4])
                    feld = (heim[:-1]+str(spielernummer),feldGr[1])
            for ziel in ziele:
                if ziel == feldGr[0]:
                    spielernummer = (int(ziel[4])-playerNumber)%4
                    feld = (ziel[:-1]+str(spielernummer),feldGr[1])
            figuren.append(Figur((figure.get_spielernummer()-playerNumber)%4, figure.get_figurenrnummer() ,feld))
        board = Board(figuren)
        game = Game(None, None, None)
        figuren = tuple(figuren)
        return board, figuren, game



game = GameRunner(RandomPlayerBot(),RandomPlayerBot(),RandomPlayerBot(),RandomPlayerBot())
app = QApplication([])
w = BoardGraphic(game)
game.setGraphicBoard(w)
game.distributeCards()
w.show()

app.exec_()