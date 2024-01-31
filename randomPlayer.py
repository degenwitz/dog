import random
from Cards import Card, EasyCard, Four, Seven, King, Ass, Joker, Jack
from Figure import Figur

def print_figures(figures):
    for f in figures:
        print(f)

def is_number_move_possible(figure: Figur, board, number:int):
    if not figure.is_in_field():
        return False
    position_in_field = (figure.get_position()[1] + number )%64
    if board.get_board()[position_in_field] == None or not board.get_board()[position_in_field].is_blocking():
        return True
    else:
        return False


def random_move(card, board, figures):

    if isinstance(card, King):
        if board.get_board()[0] == None or not board.get_board()[0].is_blocking():
            card.set_exit(True)
            return card

    if isinstance(card, Jack):
        mine = None
        them = None
        for fig in figures:
            if fig.is_in_field and not fig.is_blocking():
                if fig.get_player == 0:
                    mine = fig
                if fig.get_player != 0:
                    them = fig
        if mine != None and them != None:
            card.set_my_figure(mine)
            card.set_target_figure(them)
            return card

    if isinstance(card, Four):
        for fig in figures:
            if fig.get_player == 0:
                if is_number_move_possible(fig, board, -4):
                    card.set_target_figure(fig)
                    return card

    if isinstance(card, Ass):
        for fig in figures:
            if fig.get_player == 0:
                if is_number_move_possible(fig, board, 11):
                    card.set_as_eleven()
                    card.set_target_figure(fig)
                    return card
                if is_number_move_possible(fig, board, 1):
                    card.set_as_one()
                    card.set_target_figure(fig)
                    return card

    if isinstance(card, Seven):
        l = []
        my_figs = []
        for fig in figures:
            if fig.get_player == 0 and fig.is_in_field():
                my_figs.append(fig)
        for i in range(7):
            candidate = None
            for fig in my_figs:
                if board.get_field_in_board(fig.get_position()+1) == None or (not board.get_field_in_board(fig.get_position()+1).is_blocking() and board.get_field_in_board(fig.get_position()+1).get_player() != 0):
                    candidate = fig
                    break
            if candidate == None:
                for fig in my_figs:
                    if board.get_field_in_board(fig.get_position()+1) == None or not board.get_field_in_board(fig.get_position()+1).is_blocking():
                        candidate = fig
                        break
        if not None in l:
            card.set_target_figures(l)

    if isinstance(card, EasyCard):
        for fig in figures:
            if fig.get_player() == 0:
                if is_number_move_possible(fig, board, card.get_value()):
                    card.set_target_figure(fig)
                    return card

    if isinstance(card, Joker):
        possibleCards = ( Ass("♣"), King("♣"), EasyCard(12, "♣"), EasyCard(10, "♣"), EasyCard(9, "♣"), EasyCard(8, "♣"), Seven("♣"), EasyCard(6, "♣"), EasyCard(5, "♣"), Four(12, "♣"), EasyCard(3, "♣"), EasyCard(2, "♣"),)
        for pos_card in possibleCards:
            new_card = random_move(pos_car, board, figures)
            card.set_card(new_card)
            return card


    raise Exception('No legal move found')

def get_playable_cards(hand, board, figures):
    possible_cards = []
    for card in hand:
        try:
            random_move(card, board, figures)
            possible_cards.append(card)
        except Exception as error:
            pass
    return possible_cards

class RandomPlayerBot():

    def playCard(self, hand, board, figures, game):

        playable_cards = get_playable_cards(hand, board, figures)

        chosen_card = random.choice(playable_cards)

        return random_move(chosen_card, board, figures)

    def swapCard(self, hand, board, figures, game):
        return random.choice(hand)
