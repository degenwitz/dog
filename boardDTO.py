from global_vals import spielfeld, zuhause, ziele

class Board:

  def __init__(self, figures):
    self.board = [None]*16*4
    self.homes = [[None]*4]*4
    self.goals = [[None]*4]*4
    for figur in figures:
      pos = figur.get_position()
      if( pos[0] == spielfeld):
        self.board[pos[1]] = figur
      i = 0
      for heim in zuhause:
        if heim == pos[0]:
          self.homes[i][pos[1]] = figur
        i += 1
      i = 0
      for ziel in ziele:
        if ziel == pos[0]:
          self.goals[i][pos[1]] = figur
        i += 1

  def get_board(self):
    return self.board

  def get_field_in_board(self, i):
    return self.board[i%64]

  def get_goal_fiel_player(self, playernumber:int, fieldnumber:int):
    return  self.goals[fieldnumber][playernumber]