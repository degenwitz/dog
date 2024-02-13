from board import (FigureButton, BoardGraphic)
from boardDTO import Board
from PyQt5.QtWidgets import QApplication
from playerClass import PlayerClass
from randomPlayer import RandomPlayerBot, get_playable_cards
from Cards import Card, EasyCard, Four, Seven, King, Ass, Joker, Jack
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
                deck.append(Jack(color))
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
        self.__still_need_to_swap_cards = True

        self.currentHandSize -= 1
        if self.currentHandSize < 2:
            self.currentHandSize = 5

    def figur_bewegen(self, playerNumber, card):
        figure = self.boardGraphic.getFigure(card.get_target_figure(),playerNumber)
        figure.ziehen(card.get_value(), card.get_enter_if_possible() )
        for figs in self.boardGraphic.getFigures():
            if figs != figure and figs.get_aktuelles_feld()[0] == 'Spielfeld' and figure.get_aktuelles_feld()[0] == 'Spielfeld' and figs.get_aktuelles_feld()[1] == figure.get_aktuelles_feld()[1]:
                figs.nach_hause()


    def executeCard(self, playerNumber, card):

        #handles ass and king
        if isinstance(card, King) == True:
            if card.get_exit():
                for figs in self.boardGraphic.getFigures():
                    if figs.get_spielernummer() == playerNumber:
                        if figs.get_aktuelles_feld()[0] in zuhause:
                            figs.rauskommen()
                            return
            else:
                self.figur_bewegen(playerNumber, card)
                return

        if isinstance(card, Four):
            if card.get_move_back():
                figure = self.boardGraphic.getFigure(card.get_target_figure(),playerNumber)
                feld_zahl = (figure.get_aktuelles_feld()[1] - 4)%64
                figure.ins_feld_setzen(feld_zahl)
                for figs in self.boardGraphic.getFigures():
                    if figs != figure and figs.get_aktuelles_feld()[0] == 'Spielfeld' and figs.get_aktuelles_feld()[1] == figure.get_aktuelles_feld()[1]:
                        figs.nach_hause()
                return 
            else:
                self.figur_bewegen(playerNumber, card)
                return

        if isinstance(card, Seven):
            for (figs, enter_goal) in card.get_target_figures():
                eins = EasyCard(card.get_color(), 1)
                eins.set_enter_if_possible( enter_goal )
                eins.set_target_figure(figs)
                self.figur_bewegen(playerNumber, eins)
            return

        if isinstance(card, EasyCard) and card.get_target_figure() != None:
            self.figur_bewegen(playerNumber, card)
            return


        if isinstance(card, Jack):
            my_fig, other_fig = card.get_swap_figures()
            pos1 = (my_fig.get_position()[1]+16*playerNumber)%64
            pos2 = (other_fig.get_position()[1]+16*playerNumber)%64
            figure1 = self.boardGraphic.getFigure(my_fig,playerNumber)
            figure2 = self.boardGraphic.getFigure(other_fig,playerNumber)
            figure1.ins_feld_setzen(pos2)
            figure2.ins_feld_setzen(pos1)
            return

        if isinstance(card, Joker):
            self.executeCard(playerNumber, card.get_card() )
            return

        raise Exception('No way to play card found for card ' + str(card) )

    def swap_command_for_player(self, i:int):
            cards = self.players[i].getHand()
            board, figuren, game = self.generatePlayerObjects(i)
            swapedCard = self.playersBots[i].swapCard(cards, board, figuren, game)
            return swapedCard

    def nextMove(self):
        if( self.__still_need_to_swap_cards):
            cards = {}
            for player in range(4):
                cards[ (player, (player+2)%4) ] = self.swap_command_for_player(player)
            for partners, card in cards.items():
                self.players[partners[0]].removeCard(card)
                self.players[partners[1]].addCard(card)
                self.boardGraphic.addCard(card,("player", partners[1]))
            self.__still_need_to_swap_cards = False
        else:
            cards = self.players[self.currentPlayer].getHand()
            if len(cards) != 0:
                board, figuren, game = self.generatePlayerObjects(self.currentPlayer)
                if len(get_playable_cards(cards, board, figuren)) == 0:
                    for card in cards:
                        self.players[self.currentPlayer].removeCard(card)
                        self.discard += (card,)
                        self.boardGraphic.addCard(card, ("discard",) )
                else:
                    playedCard = self.playersBots[self.currentPlayer].playCard(cards, board, figuren, game)
                    self.executeCard(self.currentPlayer, playedCard)
                    self.players[self.currentPlayer].removeCard(playedCard)
                    self.discard += (playedCard,)
                    self.boardGraphic.addCard(playedCard, ("discard",) )
            self.__increase_turn()


    def __increase_turn(self):
        self.set_turn((self.currentPlayer + 1)%4)

    def set_turn(self, i:int):
        self.currentPlayer = i
        self.boardGraphic.set_current_player(self.currentPlayer)


    def setGraphicBoard(self, boardGraphic):
        self.boardGraphic = boardGraphic
        i = 0
        for player in self.players:
            player.set_graphic( boardGraphic.get_player_graphic(i) )
            i+=1

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
            not_graphic_figur = Figur((figure.get_spielernummer()-playerNumber)%4, figure.get_figurenrnummer() ,feld)
            not_graphic_figur.set_blocking( figure.ist_blockierend() )
            figuren.append(not_graphic_figur)
        board = Board(figuren)
        game = Game(None, None, None)
        figuren = tuple(figuren)
        return board, figuren, game

    def get_all_cards(self):
        return self.deck + self.discard + self.players[0].getHand()+ self.players[1].getHand()+ self.players[2].getHand()+ self.players[3].getHand()

    def init_game(self):
        self.distributeCards()
        self.boardGraphic.set_pile(self.deck, ("deck",) )
        self.set_turn(0)

    def skipTurn(self):
        self.__increase_turn()

    def __remove_old_owner_of_card(self, card:Card):
        for player in self.players:
            if card in player.getHand():
                player.removeCard(card, allertGraphic=False)
        if card in self.deck:
            deck = list(self.deck)
            deck.remove(card)
            self.deck = tuple(deck)
        if card in self.discard:
            discard = list(self.discard)
            discard.remove(card)
            self.discard = tuple(discard)

    def set_player_card(self, player_number:int, card:Card):
        self.__remove_old_owner_of_card(card)
        self.players[player_number].addCard(card, allertGraphic=False)

    def set_deck_card(self, card:Card, i):
        self.__remove_old_owner_of_card(card)
        deck = list(self.deck)
        if i < len(deck):
            deck.insert(i, card)
        else:
            deck.append(card)
        self.deck = tuple(deck)

    def set_discard_card(self, card:Card, i):
        self.__remove_old_owner_of_card(card)
        discard = list(self.discard)
        if i < len(discard):
            discard.insert(i, card)
        else:
            discard.append(card)
        self.discard = tuple(discard)


game = GameRunner(RandomPlayerBot(),RandomPlayerBot(),RandomPlayerBot(),RandomPlayerBot())
app = QApplication([])
w = BoardGraphic(game)
game.setGraphicBoard(w)
game.init_game()
w.show()

app.exec_()
