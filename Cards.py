from Figure import Figur

class Card:
    def __init__(self, color):
        self.__color = color
        self.enter_if_possible = True

    def get_color(self):
        return self.__color

    def get_enter_if_possible(self):
        return self.enter_if_possible

    def set_enter_if_possible(self, enter: bool):
        self.enter_if_possible = enter

    def key(self):
        return (self.__color, str(type(self)))

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.key() == other.key()
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

  def key(self):
    return unicodeCards[(self.get_color(), 13)]

class Ass(King):
  def __init__(self, color):
    super().__init__(color)
    self.value = 11

  def key(self):
    return unicodeCards[(self.get_color(), 1)]

class Seven(Card):
  def __init__(self, color):
    super().__init__(color)

  def key(self):
    return unicodeCards[(self.get_color(), 7)]

class Jack(Card):
  def __init__(self, color):
    super().__init__(color)

  def key(self):
    return unicodeCards[(self.get_color(), 11)]

class Joker(Card):
  def __init__(self, color):
    super().__init__(color)

  def __init__(self):
        super().__init__("🃏")
        pass

  def key(self):
    return "🃏"

unicodeCards = {}
color_unicode = {"♣": 127184, "♢": 127168, "♡": 127152, "♠": 127136}
spades = 127136
num_to_char = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:13, 13:14}
for color, base_value in color_unicode.items():
    for i in range(1, 14):
        unicodeCards[(color,i)] = str(chr(base_value+num_to_char[i]))