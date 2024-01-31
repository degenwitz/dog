from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData, QSize, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QIcon, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from Cards import Card
import csv
import random
from Figure import Figur


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


class NextPlayerButton(QPushButton):

    def __init__(self, game, window):
        super().__init__("next move", window)
        self.game = game
        self.move(500,500)

    def onClick(self):
        self.game.nextMove()


class SkipTurnButton(QPushButton):

    def __init__(self, game, window):
        super().__init__("skip turn", window)
        self.game = game
        self.move(500,450)

    def onClick(self):
        self.game.skipTurn()


class FigureButton(QPushButton):

    def __init__(self, spieler, nummer, window):
        super().__init__("", window)
        self.setIcon(QIcon(tokens[spieler]))
        self.setIconSize(QSize(22,22))
        self.setStyleSheet("background: transparent; border : 0")
        self.spieler = spieler
        self.nummer = nummer
        self.mein_feld = (zuhause[spieler], nummer)
        self.blockt = True
        pos = felder[zuhause[spieler]][nummer]
        self.move(pos[0],pos[1])


    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            
            self.render(pixmap)

            drag.setPixmap(pixmap)
            drag.setHotSpot(
                QPoint(self.width() // 2, self.height() // 2)
            )

            drag.exec_(Qt.MoveAction)

    def setzen(self, art, feld_nummer):
        self.mein_feld = (art, feld_nummer)
        pos = felder[art][feld_nummer]
        self.move(pos[0],pos[1])
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


class CardGraphic(QPushButton):

    def __init__(self, card: Card, poition, window):
        super().__init__(str(card), window)
        self.__position = poition
        self.move(poition[0],poition[1])
        self.setFont(QFont('Times', 30))
        self.card = card

    def is_card(self, card:Card):
        return card == self.card


    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.exec_(Qt.MoveAction)

    def my_move(self, position):
        self.move(position[0], position[1])


class PlayerGraphic():

    def best_dinstance(position: int):
        for i in range(4):
            if position < 80 + i*80:
                return i
        return -1


    def __init__(self, playernumer: int, window, set_player):
        self.__playernumber = playernumer
        self.__hand = []

        self.__player_indicator = QPushButton("", window)
        self.__player_indicator.setIcon(QIcon(tokens[playernumer]))
        self.__player_indicator.setIconSize(QSize(24,24))
        self.__player_indicator.move(550,10 + self.__playernumber*80)
        self.__player_indicator.clicked.connect(set_player)

        self.__current_player = QPushButton("", window)
        self.__current_player.setIcon(QIcon("startspieler_icon.jpg"))
        self.__current_player.setIconSize(QSize(24,24))
        self.__current_player.move(520,10 + self.__playernumber*80)
        self.__current_player.setVisible(False)

    def get_number():
        return self.__playernumber

    def set_as_current_player(self, isCurrentPlayer:bool):
        self.__current_player.setVisible(isCurrentPlayer)

    def add_graphic_card(self, card: CardGraphic, window):
        position = (600+len(self.__hand)*60, 10 + self.__playernumber*80)
        self.__hand.append(card)
        card.my_move(position)

    def __reorg(self):
        i = 0
        for card in self.__hand:
            position = (600+i*60, 10 + self.__playernumber*80)
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
        print("ment to remove card", str(card), "but card not found")


class Pile_Graphic():

    def __init__(self, window, name, pos_down):
        self.start_ort = pos_down
        self.__pile = []

        btn = QPushButton(name, window)
        btn.move(10, pos_down - 30)

    def calc_pos(self, i):
        x_i = i % 31
        y_i = i // 31
        return (10+x_i*60, self.start_ort+40*y_i)

    def play_into_pile(self, window, widget, position):
        height = position.x()
        width = position.y()
        i = 0
        while i < len(self.__pile):
            card = self.__pile[i]
            if card.x() < position.x() and card.x()+60 > position.x() and card.y() < position.y() and card.y() + 40 > position.y():
                break
            i += 1
        if i < len(self.__pile):
            self.__pile.insert(i, widget)
        else:
            self.__pile.append(widget)
        self.__reorg()
        return i

    def add_graphic_card(self, card: CardGraphic, window):
        self.__pile.insert(0, card)
        self.__reorg()

    def __reorg(self):
        i = 0
        for card in self.__pile:
            position = self.calc_pos(i)
            card.my_move(position)
            i += 1

    def remove_card_widget(self, card: CardGraphic, window):
        if card in self.__pile:
            self.__pile.remove(card)
            self.__reorg()

    def remove_card(self, card:Card):
        print("removing card from dicard", card)
        for card_w in self.__pile:
            if card_w.is_card(card):
                self.__pile.remove(card_w)
                self.__reorg()
                return card_w
        print("ment to remove card", str(card), "but card not found")



class BoardGraphic(QWidget):

    def __init__(self, game):
        super().__init__()
        self.setAcceptDrops(True)
        self.setGeometry(0, 0, 1000, 600)

        #Backgroud image
        # creating label
        self.label = QLabel(self)
        # loading image
        self.pixmap = QPixmap('board.png')
        # adding image to label
        self.label.setPixmap(self.pixmap)
        # Optional, resize label to image size
        self.label.resize(self.pixmap.width(),
                          self.pixmap.height())

        #self.blayout = QHBoxLayout()
        self.list = []
        j = 0
        for spieler in range(4):
            for nummer in range(4):
                btn = FigureButton(spieler, nummer,self)
                self.list.append(btn)

        #nextMoveButton
        btnMove = NextPlayerButton(game, self)
        btnMove.clicked.connect(btnMove.onClick)

        #skipTurnButton
        btnClick = SkipTurnButton(game, self)
        btnClick.clicked.connect(btnClick.onClick)

        #players
        self.__players = (PlayerGraphic(0, self, lambda: game.set_turn(0)),
                          PlayerGraphic(1, self, lambda: game.set_turn(1)),
                          PlayerGraphic(2, self, lambda: game.set_turn(2)),
                          PlayerGraphic(3, self, lambda: game.set_turn(3))
                          )

        #discard PIle
        self.discard = Pile_Graphic(self, "Ablagestapel", 750)

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

    def dragEnterEvent(self, e):
        e.accept()


    def distance(x1,y1,x2,y2):
        return (x1-x2+11)**2+(y1-y2+11)**2

    def calculate_closes_ball(pos, art, dist=1000000000, cur = None, art_alt = None):
        for i, feld in felder[art].items():
            dis_here = BoardGraphic.distance(pos.x(),pos.y(), feld[0], feld[1])
            if dis_here < dist:
                dist = dis_here
                cur = i
                art_alt = art
        return cur, dist, art_alt

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        if isinstance(widget, FigureButton):
            cur, dist, art = BoardGraphic.calculate_closes_ball(pos, spielfeld)
            for haus in zuhause:
                cur, dist, art = BoardGraphic.calculate_closes_ball(pos, haus, dist=dist, cur=cur, art_alt=art)
            for ziel in ziele:
                cur, dist, art = BoardGraphic.calculate_closes_ball(pos, ziel,dist=dist, cur=cur, art_alt=art)
            widget.setzen(art, cur)
            e.accept()
        elif isinstance(widget, CardGraphic):
            for player in self.__players:
                player.remove_card_widget(widget, self)
            self.deck.remove_card_widget(widget, self)
            self.discard.remove_card_widget(widget, self)
            if pos.x() > 500 and pos.y() < 500 :
                #spielerkarten
                newPlayer = PlayerGraphic.best_dinstance(pos.y())
                self.store_game.set_player_card(newPlayer, widget.card)
                if newPlayer >= 0:
                    self.__players[newPlayer].add_graphic_card(widget, self)
            elif pos.y() > 500 and pos.y() < 750:
                #deck
                i = self.deck.play_into_pile(self, widget, pos)
                self.store_game.set_deck_card(widget.card, i)
            elif pos.y() > 750:
                i = self.discard.play_into_pile(self, widget, pos)
                self.store_game.set_discard_card(widget.card, i)
            else:
                self.discard.add_graphic_card(widget, self)
                self.store_game.set_discard_card(widget.card, 0)
            e.accept()


    def getFigures(self):
        return self.list

    def getFigure(self, figure:Figur, playernumber:int):
        figur_playernumber = (figure.get_player()+playernumber)%4
        for fig in self.list:
            if fig.get_spielernummer() == figur_playernumber:
                if fig.get_figurenrnummer() == fig.get_figurenrnummer():
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
            for card in cards:
                card_w = self.find_card(card)
                self.discard.add_graphic_card(card_w, self)
        if(ort[0] == "deck"):
            for card in cards:
                card_w = self.find_card(card)
                self.deck.add_graphic_card(card_w, self)

    def set_current_player(self, i:int):
        for player in self.__players:
            player.set_as_current_player(False)
        self.__players[i].set_as_current_player(True)
