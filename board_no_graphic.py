from Cards import Card
import csv
import random
import threading
from Figure import Figur
from time import sleep


first_row = True
spielfeld = 'Spielfeld'
felder = {spielfeld:{}}
zuhause = ('home1', 'home2', 'home3', 'home4')
for heim in zuhause:
    felder[heim] = {}
ziele = ('goal1', 'goal2', 'goal3', 'goal4')
for ziel in ziele:
    felder[ziel] = {}

tokens = ("red_marbel.png", "yellow_marbel.png", "blue_marbel.png", "green_marbel.png", )

with open('board.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')

    for row in spamreader:
        if first_row:
            first_row = False
            continue
        felder[row[0]][int(row[1])] = (int(row[2])-11,int(row[3])-11)

class FigureButton:

    def __init__(self, spieler, nummer, window):
        self.spieler = spieler
        self.nummer = nummer
        self.mein_feld = (zuhause[spieler], nummer)
        self.blockt = True
        pos = felder[zuhause[spieler]][nummer]

    def setzen(self, art, feld_nummer):
        self.mein_feld = (art, feld_nummer)
        pos = felder[art][feld_nummer]
        if(art != spielfeld):
            self.blockt = True
        else:
            if feld_nummer != 16*self.spieler:
                self.blockt = False
            else:
                self.blockt = True

    def ins_ziel_setzen(self, ziel_nummer):
        self.setzen(ziele[self.spieler], ziel_nummer)

    def ins_feld_setzen(self, feld_nummer):
        self.setzen(spielfeld, feld_nummer)

    def nach_hause(self):
        self.setzen(zuhause[self.spieler], self.nummer)
        self.blockt = True

    def rauskommen(self):
        self.setzen(spielfeld, 16*self.spieler)
        self.blockt = True

    #überprüft nicht, ob er geblockt wird, etwas frisst oder so
    #Wenn er schon im Ziel ist, wird nicht überprüft, ob er legal viel läuft. Wenn zu weit, wird ein fehler geworfen
    def ziehen(self, wie_viel, ins_tor):
        if(self.mein_feld[0] == spielfeld):
            neues_feld = (self.mein_feld[1]+wie_viel)%64
            if(ins_tor):
                im_ziel = neues_feld - 16*self.spieler
                if not self.blockt and self.mein_feld[1] <= 16*self.spieler and im_ziel > 0 and im_ziel < 5:
                    im_ziel -= 1
                    self.ins_ziel_setzen(im_ziel)
                    return
            self.ins_feld_setzen(neues_feld)
            self.blockt = False

        if(self.mein_feld[0] == ziele[self.spieler]):
            neues_feld = self.mein_feld[1]+wie_viel
            self.setzen(self.mein_feld[0], neues_feld)

    def get_aktuelles_feld(self):
        return self.mein_feld

    def ist_blockierend(self):
        return self.blockt

    def get_spielernummer(self):
        return self.spieler

    def get_figurenrnummer(self):
        return self.nummer


class CardGraphic:

    def __init__(self, card: Card, poition, window):
        self.__position = poition
        self.card = card

    def is_card(self, card:Card):
        return card == self.card

    def my_move(self, position):
        pass


class PlayerGraphic():

    def best_dinstance(position: int):
        for i in range(4):
            if position < 80 + i*80:
                return i
        return -1


    def __init__(self, playernumer: int, window, set_player):
        self.__playernumber = playernumer
        self.__hand = []

    def get_number():
        return self.__playernumber

    def set_as_current_player(self, isCurrentPlayer:bool):
        pass

    def add_graphic_card(self, card: CardGraphic, window):
        position = (600+len(self.__hand)*45, 10 + self.__playernumber*80)
        self.__hand.append(card)
        card.my_move(position)

    def __reorg(self):
        i = 0
        for card in self.__hand:
            position = (600+i*45, 10 + self.__playernumber*80)
            card.my_move(position)
            i += 1

    def remove_card_widget(self, card: CardGraphic, window):
        if card in self.__hand:
            self.__hand.remove(card)
            self.__reorg()

    def remove_card(self, card:Card):
        for card_w in self.__hand:
            if card_w.is_card(card):
                self.__hand.remove(card_w)
                self.__reorg()
                return card_w
        s = "removing card "+ str(card.comparer()) +" cards I have: "
        for card_w in self.__hand:
            s += str(card_w.card.comparer()) + ", "
        print(s)
        print("ment to remove card", str(card.comparer()), "but card not found")


class Pile_Graphic():
    def __init__(self, window, name, pos_down):
        self.start_ort = pos_down
        self.__pile = []

    def calc_pos(self, i):
        x_i = i % 31
        y_i = i // 31
        return (10+x_i*40, self.start_ort+55*y_i)

    def add_graphic_card(self, card: CardGraphic, window):
        self.__pile.insert(0, card)
        self.__reorg()

    def clean_pile(self):
        self.__pile = []

    def __reorg(self):
        pass

    def remove_card_widget(self, card: CardGraphic, window):
        pass

    def remove_card(self, card:Card):
        for card_w in self.__pile:
            if card_w.is_card(card):
                self.__pile.remove(card_w)
                self.__reorg()
                return card_w
        print("ment to remove card", str(card), "but card not found")


class BoardGraphic: #QMainWindow): #

    def __init__(self, game):

        self.list = []
        j = 0
        for spieler in range(4):
            for nummer in range(4):
                btn = FigureButton(spieler, nummer,self)
                self.list.append(btn)

        #players
        self.__players = (PlayerGraphic(0, self, lambda: game.set_turn(0)),
                          PlayerGraphic(1, self, lambda: game.set_turn(1)),
                          PlayerGraphic(2, self, lambda: game.set_turn(2)),
                          PlayerGraphic(3, self, lambda: game.set_turn(3))
                          )

        #discard PIle
        self.discard = Pile_Graphic(self, "Ablagestapel", 770)

        #deck Pile
        self.deck = Pile_Graphic(self, "deck", 550)

        #create all cards
        self.create_all_cards(game)

        #store game
        self.store_game = game

    def create_all_cards(self, game):
        l = game.get_all_cards()
        all_cards = []
        for card in l:
            card_gr = CardGraphic(card, (0,0), self)
            all_cards.append(card_gr)
        self.all_cards = tuple(all_cards)

    def find_card(self, card:Card):
        for card_w in self.all_cards:
            if card_w.is_card(card):
                return card_w
        print("searched for card that does not exist!!!!")

    def getFigures(self):
        return self.list

    def getFigure(self, figure:Figur, playernumber:int):
        figur_playernumber = (figure.get_player()+playernumber)%4
        for fig in self.list:
            if fig.get_spielernummer() == figur_playernumber:
                if fig.get_figurenrnummer() == figure.number:
                    return fig

    def addCard(self, card:Card, ort):
        card_w = self.find_card(card)
        if(ort[0] == "player"):
            self.__players[ort[1]].add_graphic_card( card_w, self)
        if(ort[0] == "discard"):
            self.discard.add_graphic_card(card_w, self)
        if(ort[0] == "deck"):
            self.deck.add_graphic_card(card_w, self)

    def get_player_graphic(self, playernumber:int):
        return self.__players[playernumber]

    def set_pile(self, cards, ort):
        if(ort[0] == "discard"):
            self.discard.clean_pile()
            for card in cards:
                card_w = self.find_card(card)
                self.discard.add_graphic_card(card_w, self)
        if(ort[0] == "deck"):
            self.deck.clean_pile()
            for card in cards:
                card_w = self.find_card(card)
                self.deck.add_graphic_card(card_w, self)

    def set_current_player(self, i:int):
        for player in self.__players:
            player.set_as_current_player(False)
        self.__players[i].set_as_current_player(True)
