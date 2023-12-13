from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import csv
import random


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
        felder[row[0]][int(row[1])] = (int(row[2]),int(row[3]))


class DragButton(QPushButton):

    def __init__(self, spieler, nummer, window):
        super().__init__("", window)
        self.setIcon(QIcon(tokens[spieler]))
        self.setIconSize(QSize(24,24))
        self.spieler = spieler
        self.nummer = nummer
        self.mein_feld = (ziele[spieler], nummer)
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

    #überprüft nicht, ob er geblockt wird, etwas frisst oder so
    #Wenn er schon im Ziel ist, wird nicht überprüft, ob er legal viel läuft. Wenn zu weit, wird ein fehler geworfen
    def ziehen(self, wie_viel, ins_tor):
        if(self.mein_feld[0] == spielfeld):
            neues_feld = (self.mein_feld[1]+wie_viel)%64
            if(ins_tor):
                im_ziel = neues_feld - 16*self.spieler
                print(im_ziel)
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


class Window(QWidget):

    def __init__(self):
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
                btn = DragButton(spieler, nummer,self)
                self.list.append(btn)

        #self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()


    def distance(x1,y1,x2,y2):
        return (x1-x2+12)**2+(y1-y2+12)**2

    def calculate_closes_ball(pos, art, dist=1000000000, cur = None, art_alt = None):
        for i, feld in felder[art].items():
            dis_here = Window.distance(pos.x(),pos.y(), feld[0], feld[1])
            if dis_here < dist:
                dist = dis_here
                cur = i
                art_alt = art
        return cur, dist, art_alt

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        cur, dist, art = Window.calculate_closes_ball(pos, spielfeld)
        for haus in zuhause:
            cur, dist, art = Window.calculate_closes_ball(pos, haus, dist=dist, cur=cur, art_alt=art)
        for ziel in ziele:
            cur, dist, art = Window.calculate_closes_ball(pos, ziel,dist=dist, cur=cur, art_alt=art)

        widget.setzen(art, cur)

        e.accept()

app = QApplication([])
w = Window()
w.show()

app.exec_()