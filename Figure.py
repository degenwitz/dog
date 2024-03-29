from global_vals import spielfeld, zuhause, ziele

class Figur:
  def __init__(self, player:int, number: int, field: tuple):
    self.player = player
    self.number = number
    self.field = field
    self.rausgekommen = True
    pass

  def get_position(self):
    return self.field

  def set_position(self, field: tuple):
    self.field = field

  def __str__(self):
    return "player: " + str(self.player) + " num: " + str(self.number) + " feld: " + str(self.field)

  def get_player(self):
    return self.player

  def get_number(self):
    return self.number

  def is_in_field(self):
    return self.field[0] == spielfeld

  def is_home(self):
    return self.field[0] in zuhause

  def is_in_goal(self):
    return self.field[0] in ziele

  def set_blocking(self, val):
    self.rausgekommen = val

  def is_blocking(self):
    return self.rausgekommen