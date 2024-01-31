import random
from Cards import Card, EasyCard, Four, Seven, King, Ass, Joker

def print_figures(figures):
    for f in figures:
        print(f)

class RandomPlayerBot():

    def playCard(self, hand, board, figures, game):
        for card in hand:
            if isinstance(card, King):
                return card
        for fig in figures:
            if fig.get_player() == 0:
                if fig.is_in_field():
                    for card in hand:
                        if isinstance(card, EasyCard):
                            card.set_target_figure(fig)
                            return card

        return random.choice(hand)