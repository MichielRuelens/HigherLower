from base.cards.deck import Deck
from base.cards.stack import Stack
from base.enums.game_phase import GamePhase


class Board:

    def __init__(self, deck: Deck):
        self.deck = deck
        self.stack = Stack()
        self.phase = None

    def set_phase(self, game_phase: GamePhase):
        self.phase = game_phase

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = ""
        print_str += "-------------------- BOARD ----------------------" + "\n"
        print_str += "Deck: {} cards left".format(self.deck.num_cards()) + "\n"
        print_str += "{}".format(self.stack) + "\n"
        print_str += "------------------------------------------------" + "\n"
        return print_str
