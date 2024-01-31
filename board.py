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
            drag.setHotSpot( QPoint( self.width() / 2, self.height() / 2 ) );
            drag.setPixmap(pixmap)

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


    def __init__(self, playernumer: int, window):
        self.__playernumber = playernumer
        self.__hand = []

        self.__player_indicator = QPushButton("", window)
        self.__player_indicator.setIcon(QIcon(tokens[playernumer]))
        self.__player_indicator.setIconSize(QSize(24,24))
        self.__player_indicator.move(550,10 + self.__playernumber*80)

    def get_number():
        return self.__playernumber

    def add_card(self, card: Card, window):
        position = (600+len(self.__hand)*60, 10 + self.__playernumber*80)
        self.__hand.append(CardGraphic(card, position ,window))

    def add_graphic_card(self, card: CardGraphic, window):
        print("adding graphic card")
        position = (600+len(self.__hand)*60, 10 + self.__playernumber*80)
        self.__hand.append(card)
        card.my_move(position)

    def __reorg(self):
        i = 0
        for card in self.__hand:
            position = (600+i*60, 10 + self.__playernumber*80)
            card.my_move(position)
            i += 1

    def remove_card(self, card: Card, window):
        if card in self.__hand:
            self.__hand.remove(card)
            self.__reorg()



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

        #players
        self.__players = (PlayerGraphic(0, self), PlayerGraphic(1, self), PlayerGraphic(2, self), PlayerGraphic(3, self))

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
            newPlayer = PlayerGraphic.best_dinstance(pos.y())
            print(newPlayer)
            if newPlayer >= 0:
                for player in self.__players:
                    player.remove_card(widget, self)
                self.__players[newPlayer].add_graphic_card(widget, self)



    def getFigures(self):
        return self.list

    def getFigure(self, figure:Figur, playernumber:int):
        figur_playernumber = (figure.get_player()+playernumber)%4
        for fig in self.list:
            if fig.get_spielernummer() == figur_playernumber:
                if fig.get_figurenrnummer() == fig.get_figurenrnummer():
                    return fig

    def addCard(self, card:Card, ort):
        if(ort[0] == "player"):
            self.__players[ort[1]].add_card( card, self)
