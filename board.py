from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import csv
import random


first_row = True
felder = {'Spielfeld':{}, }
with open('board.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')

    for row in spamreader:
        if first_row:
            first_row = False
            continue
        felder[row[0]][int(row[1])] = (int(row[2]),int(row[3]))

print(felder)

class DragButton(QPushButton):

    def __init__(self, label, window):
        super().__init__(label, window)
        self.setIcon(QIcon('red_marbel.png'))
        self.setIconSize(QSize(24,24))

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

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
        for l in range(4):
            i = random.randrange(0,64)
            btn = DragButton("",self)
            place = felder['Spielfeld'][i]
            btn.move(place[0],place[1])
            self.list.append(btn)

        #self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()


    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        cur = None
        dist = 1000000000000
        for i, feld in felder['Spielfeld'].items():
            print(feld)
            dis_here = (pos.x()-feld[0]+12)**2+(pos.y()-feld[1]+12)**2
            if dis_here < dist:
                dist = dis_here
                cur = feld
        widget.move(cur[0],cur[1])

        e.accept()

app = QApplication([])
w = Window()
w.show()

app.exec_()