from Figure import Figur
import uuid

generatedID = 0

class Card:

    def __init__(self, color):
        self.__color = color
        self.enter_if_possible = True
        self.uuid = Card.generateID()

    def generateID():
        global generatedID
        generatedID += 1
        return generatedID


    def get_color(self):
        return self.__color

    def get_enter_if_possible(self):
        return self.enter_if_possible

    def set_enter_if_possible(self, enter: bool):
        self.enter_if_possible = enter

    def key(self):
        return (self.__color, str(type(self)))

    def comparer(self):
        return (self.key(), self.uuid)

    def __hash__(self):
        return hash(self.comparer())

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.comparer() == other.comparer()
        return NotImplemented

    def __str__(self):
        return str(self.key())


class EasyCard(Card):
  def __init__(self, color:str, value:int):
    super().__init__(color)
    self.value = value
    self.target_figure = None

  def get_value(self):
    return self.value
  
  def get_target_figure(self):
    return self.target_figure

  def set_target_figure(self, figure:Figur):
    self.target_figure = figure

  def key(self):
    return unicodeCards[(self.get_color(), self.get_value())]

class Four(EasyCard):
    def __init__(self, color):
        super().__init__(color, 4)

class King(EasyCard):
  def __init__(self, color):
    super().__init__(color, 13)
    self.exit = True

  def get_exit(self):
      return self.exit

  def set_exit(self, val):
      self.exit = val

  def key(self):
    return unicodeCards[(self.get_color(), 13)]

class Ass(King):
  def __init__(self, color):
    super().__init__(color)
    self.value = 11

  def key(self):
    return unicodeCards[(self.get_color(), 1)]

  def set_as_eleven(self):
      self.value = 11

  def set_as_one(self):
      self.value = 1

class Seven(Card):
  def __init__(self, color):
    super().__init__(color)
    self.figures = []

  def key(self):
    return unicodeCards[(self.get_color(), 7)]

  def set_target_figures(figures:list):
    self.figures = []



class Jack(Card):
  def __init__(self, color):
    super().__init__(color)

  def set_my_figure(figure:Figur):
      self.my_fig = figure

  def set_other_figure(figure:Figur):
      self.op_fig = figure

  def key(self):
    return unicodeCards[(self.get_color(), 11)]

class Joker(Card):
  def __init__(self, color):
    super().__init__(color)

  def __init__(self):
        super().__init__("🃏")
        pass

  def set_card(self, card:Card):
      self.card = card

  def get_card(self):
      return self.card

  def key(self):
    return "🃏"

unicodeCards = {}
color_unicode = {"♣": 127184, "♢": 127168, "♡": 127152, "♠": 127136}
spades = 127136
num_to_char = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:13, 13:14}
for color, base_value in color_unicode.items():
    for i in range(1, 14):
        unicodeCards[(color,i)] = str(chr(base_value+num_to_char[i]))