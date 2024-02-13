import random
from Cards import Card, EasyCard, Four, Seven, King, Ass, Joker, Jack
from global_vals import spielfeld, zuhause, ziele
from Figure import Figur
from random_player_exception import Card_not_playble
import copy

def print_figures(figures):
    for f in figures:
        print(f)

def is_number_move_possible(figure: Figur, board, number:int, entergGaol=True):

    if figure.is_home():
        return False

    startField = figure.get_position()[1]
    if startField == 0 and not figure.is_blocking():
        startField = 64
    if figure.is_in_goal():
        startField = 64 + startField

    r = range(1, number+1)
    if number < 0:
        r = range(-1, number-1, -1)
    for i in r:
        step_field = startField + i
        if step_field >= 65 and (entergGaol or figure.is_in_goal() ):
            if step_field > 68:
                return False
            else:
                continue
        else:
            step_field = step_field%64
            if board.get_board()[step_field] != None and board.get_board()[step_field].is_blocking():
                return False

    position_in_field = startField + number

    if (entergGaol or figure.is_in_goal()) and position_in_field >= 65:
        if position_in_field >= 68:
            return False
        else:
            position_in_field -= 64
            if board.get_goal_fiel_player(0, position_in_field) == None or not board.get_goal_fiel_player(0, position_in_field).is_blocking():
                return True
            else:
                return False
    else:
        position_in_field = position_in_field%64
        if board.get_board()[position_in_field] == None or not board.get_board()[position_in_field].is_blocking():
            return True
        else:
            return False


def copy_board(board, figure):
    board = copy.deepcopy(board)
    for field in board.get_board():
        if field != None and field.get_player() == figure.get_player() and field.get_number() == figure.get_number():
            figure = field
            break
    for i in range(0,4):
        field = board.get_goal_fiel_player(0,i)
        if field != None and field.get_player() == figure.get_player() and field.get_number() == figure.get_number():
            figure = field
            break
    return (board, figure)


#returns list: [ (how_much_can_walk, ((figur, go_in), (figut_go_in), ...), changedBoad),  ]
def handle_seven(board_org, figure_org, whats_left:int, eatown = False):

    if figure_org.is_in_goal():
        (board, figure) = copy_board(board_org, figure_org)
        could_walk = 0
        walked_figures = []
        for goalfield in range(figure.get_position()[1]+1, figure.get_position()[1]+whats_left+1):
            if goalfield < 4 and board.get_goal_fiel_player(0, goalfield) == None:
                could_walk += 1
                walked_figures.append( (figure, True) )
            else:
                break
        if could_walk == 0:
            return []
        else:
            figure.set_position((ziele[0], figure.get_position()[1]+could_walk))
            board.place_figure(figure)
            return [ (could_walk ,walked_figures, board), ]
    elif figure_org.is_in_field():
        returner = []
        pos = figure_org.get_position()[1]
        if  (pos + whats_left > 64 or (pos == 0 and not figure_org.is_blocking())) and board_org.get_goal_fiel_player(0,0) == None:
            (board, figure) = copy_board(board_org, figure_org)
            if figure.get_position()[1] == 0:
                pos = 65
            could_walk = 0
            walked_figures = []
            for i in range(pos+1, pos+whats_left+1):
                if i > 68:
                    break
                if i > 64:
                    can_walk = board.get_goal_fiel_player(0, i-65) == None
                else:
                    can_walk = board.get_board()[i%64] == None or board.get_board()[i%64].get_player() != 0 or (eatown and not board.get_board()[i%64].is_blocking() )
                if can_walk:
                    could_walk += 1
                    walked_figures.append( (figure, True) )
                else:
                    break
            if pos + could_walk > 64:
                figure.set_position((ziele[0], (pos+could_walk-65) ))
                board.place_figure(figure)
                returner.append( (could_walk ,walked_figures, board) )

        (board, figure) = copy_board(board_org, figure_org)
        pos = figure.get_position()[1]
        could_walk = 0
        walked_figures = []
        for i in range(pos+1, pos+whats_left+1):
            can_walk = (board.get_board()[i%64] == None or
                        (not board.get_board()[i%64].is_blocking() and
                         (board.get_board()[i%64].get_player() != 0 or eatown  )
                         ))
            if can_walk:
                could_walk += 1
                walked_figures.append( (figure, False) )
            else:
                break
        if could_walk > 0:
            figure.set_position( (spielfeld, (figure.get_position()[1]+could_walk)%64 ) )
            board.place_figure(figure)
            returner.append( (could_walk ,walked_figures, board) )
        return returner
    else:
        return []


def get_random_seven_move(card, board, move=7):
    my_figs = []
    for i in range(0,4):
        field = board.get_goal_fiel_player(0,i)
        if field != None and field.get_player() == 0:
            my_figs.append(field)
    for player in board.get_board():
        if player != None and player.get_player() == 0:
            my_figs.append(player)

    #try without eating own:
    for fig in my_figs:
        v = handle_seven(board, fig, move, False)
        for i in range(len(v)):
            plan = v[i]
            if(move-plan[0] == 0):
                if move==7:
                    card.set_target_figures(plan[1])
                    return card
                else:
                    return plan[1]
            else:
                l = plan[1]
                next_steps = get_random_seven_move(card, plan[2], move-plan[0])
                if len(next_steps) > 0:
                    l += next_steps
                    if move==7:
                        card.set_target_figures(l)
                        return card
                    else:
                        return l

    #try eating own:
    for fig in my_figs:
        v = handle_seven(board, fig, move, True)
        for i in range(len(v)):
            plan = v[i]
            if(move-plan[0] == 0):
                if move==7:
                    card.set_target_figures(plan[1])
                    return card
                else:
                    return plan[1]
            else:
                l = plan[1]
                next_steps = get_random_seven_move(card, plan[2], move-plan[0])
                if len(next_steps) > 0:
                    l += next_steps
                    if move==7:
                        card.set_target_figures(l)
                        return card
                    else:
                        return l
                    
    if move == 7:
        raise Card_not_playble
    else:
        return []



def random_move(card, board, figures):

    if isinstance(card, Jack):
        mine = None
        them = None
        for fig in figures:
            if fig.is_in_field() and not fig.is_blocking():
                if fig.get_player() == 0:
                    mine = fig
                if fig.get_player() != 0:
                    them = fig
        if mine != None and them != None:
            card.set_my_figure(mine)
            card.set_other_figure(them)
            return card

    if isinstance(card, Four):
        for fig in figures:
            if fig.get_player() == 0:
                if not fig.is_in_goal() and is_number_move_possible(fig, board, -4):
                    card.set_target_figure(fig)
                    card.set_move_back(True)
                    return card
                if is_number_move_possible(fig, board, 4):
                    card.set_target_figure(fig)
                    card.set_move_back(False)
                    card.set_enter_if_possible(True)
                    return card
                if is_number_move_possible(fig, board, 4, False):
                    card.set_target_figure(fig)
                    card.set_enter_if_possible(False)
                    card.set_move_back(False)
                    return card

    if isinstance(card, Ass):
        for fig in figures:
            if fig.get_player() == 0:
                if is_number_move_possible(fig, board, 11):
                    card.set_as_eleven()
                    card.set_target_figure(fig)
                    card.set_enter_if_possible(True)
                    return card
                if is_number_move_possible(fig, board, 1):
                    card.set_as_one()
                    card.set_target_figure(fig)
                    card.set_enter_if_possible(True)
                    return card
                if is_number_move_possible(fig, board, 11, False):
                    card.set_as_eleven()
                    card.set_target_figure(fig)
                    card.set_enter_if_possible(False)
                    return card
                if is_number_move_possible(fig, board, 1, False):
                    card.set_as_one()
                    card.set_target_figure(fig)
                    card.set_enter_if_possible(False)
                    return card

    if isinstance(card, King):
        for fig in figures:
            if fig.get_player() == 0:
                if fig.is_home() and (board.get_board()[0] == None or not board.get_board()[0].is_blocking()):
                    card.set_exit(True)
                    return card
                if is_number_move_possible(fig, board, 13):
                    card.set_exit(False)
                    card.set_enter_if_possible(True)
                    card.set_target_figure(fig)
                    return card
                if is_number_move_possible(fig, board, 13, False):
                    card.set_exit(False)
                    card.set_enter_if_possible(False)
                    card.set_target_figure(fig)
                    return card

    if isinstance(card, Seven): #TODO: mit goal machen!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return get_random_seven_move(card, board)
        l = []
        my_figs = []
        for fig in figures:
            if fig.get_player() == 0 and fig.is_in_field():
                my_figs.append(fig)
        fields_moved = [0,] * len(my_figs)
        for i in range(7):
            candidate = None
            for j in range(len(my_figs)):
                field_in_board = board.get_field_in_board(my_figs[j].get_position()[1]+fields_moved[j]+1)
                if field_in_board == None or (not field_in_board.is_blocking() and field_in_board.get_player() != 0):
                    fields_moved[j] += 1
                    candidate = my_figs[j]
            if candidate == None:
                for fig in my_figs:
                    if board.get_field_in_board(fig.get_position()+1) == None or not board.get_field_in_board(fig.get_position()+1).is_blocking():
                        candidate = fig
                        break
            l.append(candidate)
        if not None in l:
            card.set_target_figures(l)
            return card

    if isinstance(card, EasyCard):
        for fig in figures:
            if fig.get_player() == 0:
                if is_number_move_possible(fig, board, card.get_value()):
                    card.set_target_figure(fig)
                    card.set_enter_if_possible(True)
                    return card
                if is_number_move_possible(fig, board, card.get_value(), False):
                    card.set_target_figure(fig)
                    card.set_enter_if_possible(False)
                    return card

    if isinstance(card, Joker):
        possibleCards = ( Ass("♣"), King("♣"), EasyCard("♣", 12), EasyCard("♣", 10), EasyCard("♣", 9), EasyCard("♣", 8), Seven("♣"), EasyCard("♣", 6), EasyCard("♣", 5), Four("♣"), EasyCard("♣", 3), EasyCard("♣", 2),)
        for pos_card in possibleCards:
            try:
                new_card = random_move(pos_card, board, figures)
                card.set_card(new_card)
                return card
            except Card_not_playble as error:
                pass



    raise Card_not_playble

def get_playable_cards(hand, board, figures):
    possible_cards = []
    for card in hand:
        try:
            random_move(card, board, figures)
            possible_cards.append(card)
        except Card_not_playble as error:
            pass
    return possible_cards

class RandomPlayerBot():

    def playCard(self, hand, board, figures, game):

        playable_cards = get_playable_cards(hand, board, figures)

        chosen_card = random.choice(playable_cards)

        return random_move(chosen_card, board, figures)

    def swapCard(self, hand, board, figures, game):
        return random.choice(hand)
